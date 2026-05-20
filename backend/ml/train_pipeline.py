"""
Advanced ML Training Pipeline
Multi-model training with comparison, evaluation, and hyperparameter tuning
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix
)
from xgboost import XGBClassifier


def load_and_preprocess_data(dataset_path: str) -> tuple:
    """Load dataset and perform preprocessing"""
    print("=" * 60)
    print("📊 LOADING AND PREPROCESSING DATA")
    print("=" * 60)

    df = pd.read_csv(dataset_path)
    print(f"Dataset shape: {df.shape}")
    print(f"Fraudulent distribution:\n{df['fraudulent'].value_counts()}")

    # Fill missing values
    df.fillna("", inplace=True)

    # Combine text features
    df["text"] = (
        df["title"] + " " +
        df["company_profile"] + " " +
        df["description"] + " " +
        df["requirements"] + " " +
        df["benefits"]
    )

    # Feature engineering - add scam indicators
    df["has_salary_info"] = df["description"].str.contains(
        r"₹|salary|lakh|per month", case=False, regex=True
    ).astype(int)

    df["text_length"] = df["text"].str.len()
    df["word_count"] = df["text"].str.split().str.len()

    print(f"\nText column created. Average length: {df['text_length'].mean():.0f} chars")
    print(f"Average word count: {df['word_count'].mean():.0f} words")

    return df


def train_models(df: pd.DataFrame, output_dir: str = "../ml_model") -> dict:
    """Train multiple models and compare performance"""
    print("\n" + "=" * 60)
    print("🧠 TRAINING MULTIPLE MODELS")
    print("=" * 60)

    X = df["text"]
    y = df["fraudulent"]

    # TF-IDF Vectorization
    print("\n📝 Vectorizing text with TF-IDF (max_features=5000)...")
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000,
        ngram_range=(1, 2),  # Unigrams and bigrams
        min_df=2,
        max_df=0.95
    )
    X_vectorized = vectorizer.fit_transform(X)
    print(f"Feature matrix shape: {X_vectorized.shape}")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTrain size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")

    # Define models
    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000, C=1.0, random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=20, random_state=42, n_jobs=-1
        ),
        "XGBoost": XGBClassifier(
            n_estimators=100, max_depth=6, learning_rate=0.1,
            random_state=42, use_label_encoder=False, eval_metric="logloss"
        )
    }

    results = {}
    best_model = None
    best_f1 = 0

    for name, model in models.items():
        print(f"\n{'─' * 40}")
        print(f"🔄 Training: {name}")
        print(f"{'─' * 40}")

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else y_pred

        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_proba)

        # Cross-validation
        cv_scores = cross_val_score(model, X_vectorized, y, cv=5, scoring="f1")

        results[name] = {
            "accuracy": round(accuracy * 100, 2),
            "precision": round(precision * 100, 2),
            "recall": round(recall * 100, 2),
            "f1_score": round(f1 * 100, 2),
            "roc_auc": round(roc_auc * 100, 2),
            "cv_f1_mean": round(cv_scores.mean() * 100, 2),
            "cv_f1_std": round(cv_scores.std() * 100, 2)
        }

        print(f"  Accuracy:  {accuracy * 100:.2f}%")
        print(f"  Precision: {precision * 100:.2f}%")
        print(f"  Recall:    {recall * 100:.2f}%")
        print(f"  F1-Score:  {f1 * 100:.2f}%")
        print(f"  ROC-AUC:   {roc_auc * 100:.2f}%")
        print(f"  CV F1:     {cv_scores.mean() * 100:.2f}% (±{cv_scores.std() * 100:.2f}%)")

        # Track best model
        if f1 > best_f1:
            best_f1 = f1
            best_model = (name, model)

    # ─── Save Best Model ──────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"🏆 BEST MODEL: {best_model[0]} (F1: {best_f1 * 100:.2f}%)")
    print("=" * 60)

    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(best_model[1], os.path.join(output_dir, "model.pkl"))
    joblib.dump(vectorizer, os.path.join(output_dir, "vectorizer.pkl"))
    print(f"\n✅ Model saved to {output_dir}/model.pkl")
    print(f"✅ Vectorizer saved to {output_dir}/vectorizer.pkl")

    # Save comparison results
    joblib.dump(results, os.path.join(output_dir, "model_comparison.pkl"))

    return results


def main():
    """Run the complete training pipeline"""
    print("\n" + "=" * 60)
    print("🚀 AI JOB SCAM DETECTION - ML TRAINING PIPELINE")
    print("=" * 60)

    # Load data
    df = load_and_preprocess_data("../dataset/fake_job_postings.csv")

    # Train models
    results = train_models(df)

    # Print comparison table
    print("\n" + "=" * 60)
    print("📊 MODEL COMPARISON SUMMARY")
    print("=" * 60)
    print(f"\n{'Model':<25} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1':<10} {'AUC':<10}")
    print("─" * 75)
    for name, metrics in results.items():
        print(
            f"{name:<25} {metrics['accuracy']:<10} {metrics['precision']:<10} "
            f"{metrics['recall']:<10} {metrics['f1_score']:<10} {metrics['roc_auc']:<10}"
        )

    print("\n✅ Training pipeline completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
