from pathlib import Path

import joblib
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent

# Accept either `models/` (default) or `model/` (team folder name).
_MODEL_SUBDIRS = ("models", "model")


def _model_candidates(filenames):
    return [BASE_DIR / sub / name for sub in _MODEL_SUBDIRS for name in filenames]


CLF_CANDIDATES = _model_candidates(
    ["olist_classifier_model.pkl", "best_clf.pkl"]
)
REG_CANDIDATES = _model_candidates(
    ["olist_regressor_model.pkl", "best_reg.pkl"]
)

# Single source of truth for High / Medium / Low (used by predict() and Streamlit heuristic).
TIER_HIGH_MIN_PROB = 0.22
TIER_MEDIUM_MIN_PROB = 0.12


def classify_delivery_tier(p_late_prob: float) -> str:
    """Map late probability in [0, 1] to risk tier — keep in sync with the trained model UI."""
    if p_late_prob >= TIER_HIGH_MIN_PROB:
        return "High"
    if p_late_prob >= TIER_MEDIUM_MIN_PROB:
        return "Medium"
    return "Low"


def _resolve_existing(candidates):
    for p in candidates:
        if p.exists():
            return p
    return None


def load_models():
    clf_path = _resolve_existing(CLF_CANDIDATES)
    reg_path = _resolve_existing(REG_CANDIDATES)
    if clf_path is None or reg_path is None:
        raise FileNotFoundError(
            "Model file(s) missing. Expected classifier/regressor in `models/` or `model/` "
            "(e.g., olist_classifier_model.pkl and olist_regressor_model.pkl)."
        )
    clf = joblib.load(clf_path)
    reg = joblib.load(reg_path)
    return clf, reg


def predict(clf, reg, input_df):
    p_late_prob = float(clf.predict_proba(input_df)[:, 1][0])
    pred_gap = float(np.clip(reg.predict(input_df), 0, None)[0])
    risk_score = p_late_prob * pred_gap
    tier = classify_delivery_tier(p_late_prob)

    return {
        "p_late_prob": round(p_late_prob, 6),
        "p_late": round(p_late_prob * 100, 1),
        "pred_gap": round(pred_gap, 2),
        "risk_score": round(risk_score, 4),
        "tier": tier,
    }