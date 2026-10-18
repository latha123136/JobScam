"""
Continuous Learning / Retraining Engine
=========================================
Pulls confirmed feedback from MongoDB, merges it with the original
dataset, retrains all three models, saves the best one, and
hot-swaps it into the live ScamDetectionEngine singleton —
all without restarting the server.

Retraining is triggered in two ways:
  1. Automatically — when confirmed feedback count crosses a threshold
     (default: every 50 new confirmed samples)
  2. Manually — via POST /api/retrain/trigger (admin API)

Flow:
  MongoDB feedback collection
        ↓
  Export confirmed labels (false_positive / false_negative / scam_report)
        ↓
  Merge with base dataset (fake_job_postings.csv)
        ↓
  Retrain Logistic Regression + Random Forest + XGBoost
        ↓
  Pick best model by F1-score
        ↓
  Save new model.pkl + vectorizer.pkl (atomic swap via temp file)
        ↓
  Call scam_engine.reload_model() → live model hot-swapped
        ↓
  Save retraining report to MongoDB retraining_logs collection
"""

import os
import pandas as pd
import numpy as np
import joblib
import asyncio
import logging
from datetime import datetime
from typing import Dict, Optional

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score
)
from xgboost import XGBClassifier

logger = logging.getLogger(__name__)

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "..", "ml_model")
DATASET_PATH = os.path.join(BASE_DIR, "..", "..", "dataset", "fake_job_postings.csv")
FEEDBACK_DATASET_PATH = os.path.join(MODEL_DIR, "feedback_data.csv")

# Minimum number of new confirmed feedback samples before auto-retrain fires
AUTO_RETRAIN_THRESHOLD = int(os.getenv("RETRAIN_THRESHOLD", "50"))


class RetrainingEngine:
    """Handles incremental model retraining from user feedback"""

    def __init__(self):
        self.is_training = False          # Guard against concurrent retrains
        self.last_retrain_time: Optional[datetime] = None
        self.last_retrain_result: Optional[Dict] = None
        self.feedback_count_at_last_retrain = 0

    # ─── Public API ──────────────────────────────────────────────────────────

    async def check_and_auto_retrain(self, feedback_collection, retraining_logs_collection):
        """
        Called after every feedback submission.
        Fires retraining only when new confirmed samples >= threshold.
        Non-blocking — runs retraining in a background thread so the
        feedback API response returns immediately.
        """
        if self.is_training:
            logger.info("Retraining already in progress, skipping auto-check.")
            return

        try:
            # Count all confirmed (non-pending) feedback with a job_text label
            confirmed_count = await feedback_collection.count_documents({
                "status": "confirmed",
                "job_text": {"$exists": True, "$ne": None},
                "correct_label": {"$in": ["scam", "legitimate"]}
            })

            new_since_last = confirmed_count - self.feedback_count_at_last_retrain

            if new_since_last >= AUTO_RETRAIN_THRESHOLD:
                logger.info(
                    f"Auto-retrain triggered: {new_since_last} new confirmed samples "
                    f"(threshold={AUTO_RETRAIN_THRESHOLD})"
                )
                # Run in background thread — don't block the event loop
                loop = asyncio.get_event_loop()
                loop.run_in_executor(
                    None,
                    lambda: asyncio.run(
                        self.run_retraining(
                            feedback_collection,
                            retraining_logs_collection,
                            triggered_by="auto"
                        )
                    )
                )
        except Exception as e:
            logger.error(f"Auto-retrain check failed: {e}")

    async def run_retraining(
        self,
        feedback_collection,
        retraining_logs_collection,
        triggered_by: str = "manual"
    ) -> Dict:
        """
        Full retraining pipeline.
        Returns a result dict with metrics and status.
        """
        if self.is_training:
            return {"status": "skipped", "reason": "Retraining already in progress"}

        self.is_training = True
        start_time = datetime.utcnow()
        logger.info(f"=== Retraining started (triggered_by={triggered_by}) ===")

        try:
            # 1. Load base dataset
            base_df = self._load_base_dataset()
            if base_df is None:
                raise FileNotFoundError(f"Base dataset not found at {DATASET_PATH}")

            # 2. Load confirmed feedback from MongoDB
            feedback_df = await self._load_feedback_data(feedback_collection)

            # 3. Merge datasets
            combined_df = self._merge_datasets(base_df, feedback_df)
            logger.info(
                f"Dataset: base={len(base_df)}, feedback={len(feedback_df)}, "
                f"combined={len(combined_df)}"
            )

            # 4. Train models and pick the best
            result = self._train_and_select_best(combined_df)

            # 5. Atomic model swap on disk
            self._atomic_save_model(result["best_model"], result["vectorizer"])

            # 6. Hot-reload into live singleton (no server restart needed)
            self._hot_reload_live_engine()

            # 7. Update bookkeeping
            self.last_retrain_time = datetime.utcnow()
            self.last_retrain_result = result["metrics"]
            confirmed_count = await feedback_collection.count_documents({
                "status": "confirmed",
                "job_text": {"$exists": True, "$ne": None},
                "correct_label": {"$in": ["scam", "legitimate"]}
            })
            self.feedback_count_at_last_retrain = confirmed_count

            # 8. Persist retraining log to MongoDB
            duration_seconds = (datetime.utcnow() - start_time).total_seconds()
            log_doc = {
                "triggered_by": triggered_by,
                "started_at": start_time.isoformat(),
                "completed_at": datetime.utcnow().isoformat(),
                "duration_seconds": round(duration_seconds, 1),
                "base_samples": len(base_df),
                "feedback_samples": len(feedback_df),
                "total_samples": len(combined_df),
                "best_model": result["best_model_name"],
                "metrics": result["metrics"],
                "all_model_metrics": result["all_metrics"],
                "status": "success"
            }
            await retraining_logs_collection.insert_one(log_doc)

            logger.info(
                f"=== Retraining complete in {duration_seconds:.1f}s — "
                f"Best: {result['best_model_name']} "
                f"F1={result['metrics']['f1_score']}% ==="
            )

            return {
                "status": "success",
                "best_model": result["best_model_name"],
                "metrics": result["metrics"],
                "all_metrics": result["all_metrics"],
                "samples_used": len(combined_df),
                "feedback_samples_added": len(feedback_df),
                "duration_seconds": round(duration_seconds, 1),
                "completed_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Retraining failed: {e}", exc_info=True)
            # Log failure to MongoDB
            try:
                await retraining_logs_collection.insert_one({
                    "triggered_by": triggered_by,
                    "started_at": start_time.isoformat(),
                    "failed_at": datetime.utcnow().isoformat(),
                    "error": str(e),
                    "status": "failed"
                })
            except Exception:
                pass
            return {"status": "failed", "error": str(e)}

        finally:
            self.is_training = False

    # ─── Private Methods ─────────────────────────────────────────────────────

    def _load_base_dataset(self) -> Optional[pd.DataFrame]:
        """Load and preprocess the original training CSV"""
        if not os.path.exists(DATASET_PATH):
            logger.error(f"Dataset not found: {DATASET_PATH}")
            return None

        df = pd.read_csv(DATASET_PATH)
        df.fillna("", inplace=True)

        # Combine text columns exactly as in original train_pipeline.py
        df["text"] = (
            df["title"].astype(str) + " " +
            df["company_profile"].astype(str) + " " +
            df["description"].astype(str) + " " +
            df["requirements"].astype(str) + " " +
            df["benefits"].astype(str)
        )

        # Keep only what we need
        return df[["text", "fraudulent"]].rename(columns={"fraudulent": "label"})

    async def _load_feedback_data(self, feedback_collection) -> pd.DataFrame:
        """
        Pull confirmed feedback from MongoDB.
        Only uses entries that have:
          - status == "confirmed"
          - job_text not null
          - correct_label in ["scam", "legitimate"]
        """
        rows = []
        try:
            cursor = feedback_collection.find({
                "status": "confirmed",
                "job_text": {"$exists": True, "$ne": None, "$ne": ""},
                "correct_label": {"$in": ["scam", "legitimate"]}
            })
            async for doc in cursor:
                label = 1 if doc["correct_label"] == "scam" else 0
                rows.append({
                    "text": str(doc["job_text"]),
                    "label": label,
                    "source": "feedback"
                })

            # Also pull scam reports (description field, always label=1)
            cursor2 = feedback_collection.find({
                "description": {"$exists": True, "$ne": None, "$ne": ""},
                "status": {"$in": ["confirmed", "verified"]},
                # Distinguish scam reports from feedback by absence of correct_label
                "correct_label": {"$exists": False}
            })
            async for doc in cursor2:
                rows.append({
                    "text": str(doc.get("description", "")),
                    "label": 1,  # All verified scam reports are label=1
                    "source": "scam_report"
                })

        except Exception as e:
            logger.warning(f"Could not load feedback from MongoDB: {e}")

        if not rows:
            return pd.DataFrame(columns=["text", "label"])

        df = pd.DataFrame(rows)
        df = df[df["text"].str.strip().str.len() > 20]  # Drop very short entries

        logger.info(
            f"Loaded {len(df)} feedback samples "
            f"({df['label'].sum()} scam, {(df['label']==0).sum()} legitimate)"
        )

        # Persist a local CSV backup of feedback data
        os.makedirs(MODEL_DIR, exist_ok=True)
        df.to_csv(FEEDBACK_DATASET_PATH, index=False)

        return df[["text", "label"]]

    def _merge_datasets(self, base_df: pd.DataFrame, feedback_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge base dataset with feedback.
        Feedback samples are upsampled 3x to give them more influence
        on the retrained model without needing a huge volume of corrections.
        """
        if feedback_df.empty:
            return base_df

        # Upsample feedback 3x so corrections have real weight
        feedback_upsampled = pd.concat([feedback_df] * 3, ignore_index=True)

        combined = pd.concat([base_df, feedback_upsampled], ignore_index=True)
        combined = combined.dropna(subset=["text", "label"])
        combined = combined[combined["text"].str.strip().str.len() > 10]
        combined = combined.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle

        return combined

    def _train_and_select_best(self, df: pd.DataFrame) -> Dict:
        """
        Train 3 models, evaluate, pick best by F1.
        Returns dict with best model, vectorizer, and all metrics.
        """
        X = df["text"]
        y = df["label"].astype(int)

        # Vectorize
        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95
        )
        X_vec = vectorizer.fit_transform(X)

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_vec, y, test_size=0.2, random_state=42, stratify=y
        )

        # Class imbalance ratio
        neg_count = int((y == 0).sum())
        pos_count = int((y == 1).sum())
        scale_pos = round(neg_count / max(pos_count, 1), 2)

        models = {
            "Logistic Regression": LogisticRegression(
                max_iter=1000, C=1.0, random_state=42,
                class_weight="balanced"
            ),
            "Random Forest": RandomForestClassifier(
                n_estimators=100, max_depth=20, random_state=42, n_jobs=-1,
                class_weight="balanced"
            ),
            "XGBoost": XGBClassifier(
                n_estimators=100, max_depth=6, learning_rate=0.1,
                random_state=42, use_label_encoder=False, eval_metric="logloss",
                verbosity=0, scale_pos_weight=scale_pos
            )
        }

        all_metrics = {}
        best_model = None
        best_model_name = None
        best_f1 = 0.0

        for name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]

            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            auc = roc_auc_score(y_test, y_proba)

            all_metrics[name] = {
                "accuracy": round(acc * 100, 2),
                "precision": round(prec * 100, 2),
                "recall": round(rec * 100, 2),
                "f1_score": round(f1 * 100, 2),
                "roc_auc": round(auc * 100, 2),
            }

            logger.info(
                f"  {name}: acc={acc*100:.1f}% f1={f1*100:.1f}% auc={auc*100:.1f}%"
            )

            if f1 > best_f1:
                best_f1 = f1
                best_model = model
                best_model_name = name

        return {
            "best_model": best_model,
            "best_model_name": best_model_name,
            "vectorizer": vectorizer,
            "metrics": all_metrics[best_model_name],
            "all_metrics": all_metrics,
        }

    def _atomic_save_model(self, model, vectorizer):
        """
        Save model and vectorizer atomically using temp files.
        This prevents a half-written model.pkl from corrupting the
        live model if the process is killed during save.
        """
        os.makedirs(MODEL_DIR, exist_ok=True)

        model_path = os.path.join(MODEL_DIR, "model.pkl")
        vec_path = os.path.join(MODEL_DIR, "vectorizer.pkl")
        model_tmp = model_path + ".tmp"
        vec_tmp = vec_path + ".tmp"

        # Write to temp files first
        joblib.dump(model, model_tmp)
        joblib.dump(vectorizer, vec_tmp)

        # Atomic rename — if this succeeds, both files are consistent
        os.replace(model_tmp, model_path)
        os.replace(vec_tmp, vec_path)

        logger.info(f"Model saved atomically to {model_path}")

    def _hot_reload_live_engine(self):
        """
        Reload model files into the live ScamDetectionEngine singleton.
        The running server immediately starts using the new model —
        no restart required.
        """
        try:
            from ml.scam_detector import scam_engine
            scam_engine.reload_model()
            logger.info("Live scam engine hot-reloaded with new model.")
        except Exception as e:
            logger.error(f"Hot-reload failed (server still running old model): {e}")


# ─── Singleton ────────────────────────────────────────────────────────────────
retraining_engine = RetrainingEngine()
