import joblib
import numpy as np
import pandas as pd

CLF_PATH = '../models/best_clf.pkl'
REG_PATH = '../models/best_reg.pkl'

def load_models():
    clf = joblib.load(CLF_PATH)
    reg = joblib.load(REG_PATH)
    return clf, reg

def predict(clf, reg, input_df):
    p_late   = clf.predict_proba(input_df)[:, 1][0]
    pred_gap = float(np.clip(reg.predict(input_df), 0, None)[0])
    risk     = p_late * pred_gap
    tier     = 'High' if risk > 0.6 else ('Medium' if risk > 0.2 else 'Low')
    return {
        'p_late':   round(p_late * 100, 1),
        'pred_gap': round(pred_gap, 2),
        'risk':     round(risk, 4),
        'tier':     tier,
    }