"""
Train tuned XGBoost classifier + regressor (NB05 hyperparameters) and save to models/.
Run from repo root:  python scripts/train_final_models.py
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier, XGBRegressor

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"


def main():
    feat_path = PROC / "olist_features.csv"
    merged_path = PROC / "olist_merged.csv"
    if not feat_path.exists() or not merged_path.exists():
        raise SystemExit(f"Missing {feat_path} or {merged_path}")

    df = pd.read_csv(feat_path)
    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "max_shipping_limit_date",
        "min_shipping_limit_date",
    ]
    df_merged = pd.read_csv(merged_path, parse_dates=date_cols)
    delay_gap = (
        df_merged["order_delivered_customer_date"] - df_merged["order_estimated_delivery_date"]
    ).dt.days.values[: len(df)]
    delay_gap = pd.Series(delay_gap, name="delay_gap")

    for col in [
        "delivery_days",
        "delivery_status",
        "review_score",
        "order_delivered_customer_date",
        "carrier_handling_days",
    ]:
        if col in df.columns:
            raise SystemExit(f"LEAKAGE: {col} must not be in features")

    X = df.drop(columns=["is_late"])
    y_class = df["is_late"]
    y_reg = delay_gap

    cat_cols = X.select_dtypes(include="object").columns.tolist()
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

    preprocessor = ColumnTransformer(
        [
            (
                "num",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                num_cols,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                    ]
                ),
                cat_cols,
            ),
        ],
        remainder="drop",
    )

    split = int(len(X) * 0.80)
    X_train = X.iloc[:split]
    y_train_c = y_class.iloc[:split]
    y_train_r = y_reg.iloc[:split]

    spw = (y_train_c == 0).sum() / max((y_train_c == 1).sum(), 1)

    # Tuned params from notebooks/05_modelling_final.ipynb (GridSearchCV outputs)
    clf = Pipeline(
        [
            ("pre", preprocessor),
            (
                "model",
                XGBClassifier(
                    n_estimators=200,
                    max_depth=6,
                    learning_rate=0.05,
                    subsample=0.8,
                    colsample_bytree=1.0,
                    scale_pos_weight=float(spw),
                    eval_metric="logloss",
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )
    reg = Pipeline(
        [
            ("pre", preprocessor),
            (
                "model",
                XGBRegressor(
                    n_estimators=300,
                    max_depth=6,
                    learning_rate=0.05,
                    subsample=0.8,
                    colsample_bytree=1.0,
                    min_child_weight=20,
                    gamma=1,
                    objective="reg:squarederror",
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    print("Fitting classifier…")
    clf.fit(X_train, y_train_c)
    print("Fitting regressor…")
    reg.fit(X_train, y_train_r)

    out_dir = ROOT / "models"
    out_dir.mkdir(parents=True, exist_ok=True)
    clf_path = out_dir / "olist_classifier_model.pkl"
    reg_path = out_dir / "olist_regressor_model.pkl"
    joblib.dump(clf, clf_path)
    joblib.dump(reg, reg_path)
    print(f"Wrote {clf_path}")
    print(f"Wrote {reg_path}")


if __name__ == "__main__":
    main()
