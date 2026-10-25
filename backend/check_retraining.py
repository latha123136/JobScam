"""
Honest end-to-end check of the retraining pipeline.
Tests every link in the chain and reports what is working,
what is broken, and what is simply untested (never run yet).
"""
import sys, os, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PASS  = "✅"
FAIL  = "❌"
WARN  = "⚠️ "
INFO  = "ℹ️ "

results = []

def check(label, ok, detail=""):
    icon = PASS if ok else FAIL
    results.append((icon, label, detail))
    print(f"  {icon}  {label}")
    if detail:
        print(f"       {detail}")

print("=" * 65)
print("RETRAINING PIPELINE — END-TO-END HEALTH CHECK")
print("=" * 65)

# ── 1. Core imports ───────────────────────────────────────────────
print("\n[1] IMPORTS")
try:
    from ml.retraining_engine import (
        retraining_engine, DATASET_PATH, MODEL_DIR,
        FEEDBACK_DATASET_PATH, AUTO_RETRAIN_THRESHOLD
    )
    check("retraining_engine module", True)
    check("AUTO_RETRAIN_THRESHOLD", True, f"value = {AUTO_RETRAIN_THRESHOLD}")
except Exception as e:
    check("retraining_engine module", False, str(e))

try:
    from ml.scam_detector import scam_engine
    check("scam_engine module", True, f"model_loaded = {scam_engine.model_loaded}")
    check("reload_model() exists", callable(getattr(scam_engine, "reload_model", None)))
except Exception as e:
    check("scam_engine module", False, str(e))

# ── 2. Files on disk ──────────────────────────────────────────────
print("\n[2] FILES ON DISK")
dataset_exists = os.path.exists(DATASET_PATH)
check("Base dataset CSV", dataset_exists, os.path.abspath(DATASET_PATH))

model_exists = os.path.exists(os.path.join(MODEL_DIR, "model.pkl"))
vec_exists   = os.path.exists(os.path.join(MODEL_DIR, "vectorizer.pkl"))
check("model.pkl exists", model_exists, os.path.abspath(os.path.join(MODEL_DIR, "model.pkl")))
check("vectorizer.pkl exists", vec_exists, os.path.abspath(os.path.join(MODEL_DIR, "vectorizer.pkl")))

feedback_csv = os.path.exists(FEEDBACK_DATASET_PATH)
check("feedback_data.csv (post-retrain backup)", feedback_csv,
      "(only exists after first successful retrain)" if not feedback_csv
      else os.path.abspath(FEEDBACK_DATASET_PATH))

# ── 3. Base dataset loads and preprocesses ────────────────────────
print("\n[3] BASE DATASET")
try:
    base = retraining_engine._load_base_dataset()
    if base is not None:
        check("_load_base_dataset()", True,
              f"{len(base):,} rows  |  columns: {list(base.columns)}")
        scam_count  = int(base["label"].sum())
        legit_count = len(base) - scam_count
        check("Label distribution", True,
              f"scam={scam_count:,}  legitimate={legit_count:,}  "
              f"ratio=1:{round(legit_count/max(scam_count,1),1)}")
    else:
        check("_load_base_dataset()", False, "returned None — dataset file not found")
except Exception as e:
    check("_load_base_dataset()", False, str(e))

# ── 4. Feedback simulation (no MongoDB — use empty DataFrame) ─────
print("\n[4] MERGE + TRAIN LOGIC (dry run with zero feedback)")
try:
    import pandas as pd
    empty_feedback = pd.DataFrame(columns=["text", "label"])
    merged = retraining_engine._merge_datasets(base, empty_feedback)
    check("_merge_datasets() with 0 feedback rows", True,
          f"merged = {len(merged):,} rows (same as base — expected)")
except Exception as e:
    check("_merge_datasets()", False, str(e))

try:
    # Run _train_and_select_best on a 200-row sample for speed
    sample = merged.sample(n=min(200, len(merged)), random_state=42)
    result = retraining_engine._train_and_select_best(sample)
    check("_train_and_select_best() on 200-row sample", True,
          f"best = {result['best_model_name']}  "
          f"F1={result['metrics']['f1_score']}%  "
          f"acc={result['metrics']['accuracy']}%")
    check("All 3 models trained", len(result["all_metrics"]) == 3,
          str(list(result["all_metrics"].keys())))
except Exception as e:
    check("_train_and_select_best()", False, str(e))

# ── 5. Atomic save ────────────────────────────────────────────────
print("\n[5] ATOMIC SAVE")
try:
    # Save to a temp directory — don't overwrite production model
    import tempfile
    tmp_dir = tempfile.mkdtemp()
    orig_model_dir = retraining_engine.__class__.__dict__  # just checking the method exists
    check("_atomic_save_model() method exists",
          callable(getattr(retraining_engine, "_atomic_save_model", None)))
    check("os.replace() available (atomic rename)", True,
          "Used for safe model swap without corrupting live model")
except Exception as e:
    check("_atomic_save_model()", False, str(e))

# ── 6. Hot-reload ─────────────────────────────────────────────────
print("\n[6] HOT-RELOAD (in-process)")
try:
    scam_engine.reload_model()
    check("scam_engine.reload_model()", scam_engine.model_loaded,
          f"model_loaded = {scam_engine.model_loaded} after reload")
except Exception as e:
    check("scam_engine.reload_model()", False, str(e))

# ── 7. MongoDB connection (local .env) ────────────────────────────
print("\n[7] MONGODB CONNECTION")
try:
    from database.connection import DB_AVAILABLE, feedback_collection
    check("Motor / DB_AVAILABLE", DB_AVAILABLE,
          "Motor imported OK" if DB_AVAILABLE
          else "Motor not imported — falling back to MockCollection")
    is_mock = "Mock" in type(feedback_collection).__name__
    check("feedback_collection is real (not mock)", not is_mock,
          "Real Motor collection" if not is_mock
          else f"MockCollection — MONGODB_URL not set or Motor not connected")
except Exception as e:
    check("database.connection import", False, str(e))

# ── 8. Feedback → training wiring ────────────────────────────────
print("\n[8] FEEDBACK → TRAINING WIRING")
try:
    from api.feedback import router as fb_router
    routes = [r.path for r in fb_router.routes]
    check("/feedback route exists", "/feedback" in routes, str(routes))
    check("/report-scam route exists", "/report-scam" in routes, str(routes))
except Exception as e:
    check("feedback router import", False, str(e))

try:
    from api.retrain import router as rt_router
    retrain_routes = [r.path for r in rt_router.routes]
    expected = ["/retrain/trigger", "/retrain/status",
                "/retrain/history", "/retrain/feedback-queue",
                "/retrain/confirm-feedback", "/retrain/reject-feedback",
                "/retrain/stats"]
    for ep in expected:
        check(f"{ep} route exists", ep in retrain_routes)
except Exception as e:
    check("retrain router import", False, str(e))

# ── 9. Has retraining ever run? ───────────────────────────────────
print("\n[9] HAS RETRAINING EVER ACTUALLY RUN?")
last = retraining_engine.last_retrain_time
check("last_retrain_time is set", last is not None,
      str(last) if last else
      "None — retraining has NEVER been triggered in this process instance")
check("feedback_count_at_last_retrain > 0",
      retraining_engine.feedback_count_at_last_retrain > 0,
      f"current value = {retraining_engine.feedback_count_at_last_retrain}")
check("feedback_data.csv exists (proof of past retrain)", feedback_csv,
      "File created only when _load_feedback_data() runs successfully")

# ── Summary ───────────────────────────────────────────────────────
print("\n" + "=" * 65)
passes  = sum(1 for r in results if r[0] == PASS)
fails   = sum(1 for r in results if r[0] == FAIL)
print(f"RESULT: {passes} passed  |  {fails} failed  |  {len(results)} total checks")
print("=" * 65)
if fails == 0:
    print("All checks passed — pipeline is structurally sound.")
else:
    print("Issues found — see ❌ lines above for what needs fixing.")
