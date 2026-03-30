from pathlib import Path

import joblib
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

CLF_CANDIDATES = [
    MODEL_DIR / "olist_classifier_model.pkl",
    MODEL_DIR / "best_clf.pkl",
]
REG_CANDIDATES = [
    MODEL_DIR / "olist_regressor_model.pkl",
    MODEL_DIR / "best_reg.pkl",
]


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
            "Model file(s) missing. Expected classifier/regressor in models/ "
            "(e.g., olist_classifier_model.pkl and olist_regressor_model.pkl)."
        )
    clf = joblib.load(clf_path)
    reg = joblib.load(reg_path)
    return clf, reg


def predict(clf, reg, input_df):
    p_late_prob = float(clf.predict_proba(input_df)[:, 1][0])
    pred_gap = float(np.clip(reg.predict(input_df), 0, None)[0])
    risk_score = p_late_prob * pred_gap

    if p_late_prob >= 0.22:
        tier = "High"
    elif p_late_prob >= 0.12:
        tier = "Medium"
    else:
        tier = "Low"

    return {
        "p_late_prob": round(p_late_prob, 6),
        "p_late": round(p_late_prob * 100, 1),
        "pred_gap": round(pred_gap, 2),
        "risk_score": round(risk_score, 4),
        "tier": tier,
    }