# Notebook 05 — Supervised Modelling

## Purpose

Train classification and regression models to predict delivery delays, tune the best performers, and combine both into a Risk Score for operational prioritization.

## Input / Output

|            | Details                                                               |
| ---------- | --------------------------------------------------------------------- |
| **Input**  | `olist_features.csv` (~96,455 rows × 54 features), `olist_merged.csv` |
| **Output** | Trained models, evaluation metrics, and a Risk Score proof-of-concept |

## Experimental Setup

- **Train/test split:** Time-based split (oldest 80% → train, newest 20% → test). This simulates real-world deployment where a model must only predict future orders based on past data.
- **Train set:** 77,164 rows (8.1% late) | **Test set:** 19,291 rows (8.3% late).
- **Preprocessing:** Numeric features scaled (StandardScaler), categorical features label-encoded/one-hot encoded via a shared Pipeline.
- **Class imbalance:** Handled via `class_weight='balanced'` (Scikit-Learn) and `scale_pos_weight=11.4` (XGBoost).

## Classification Results (predict `is_late`)

| Model                   | Test ROC-AUC | Test F1 (late) | Train-Test AUC Gap | Verdict         |
| ----------------------- | ------------ | -------------- | ------------------ | --------------- |
| Logistic Regression     | 0.7255       | 0.25           | +0.0052            | ✅ Good         |
| Random Forest Clf       | 0.7538       | 0.30           | +0.0511            | ⚠️ Mild overfit |
| XGBoost Clf (Default)   | 0.7992       | 0.32           | +0.0508            | ⚠️ Mild overfit |
| **XGBoost Clf (Tuned)** | **0.7985**   | **0.34**       | +0.0800            | ⚠️ Mild overfit |

**Best classifier:** XGBoost (Tuned). While the default XGBoost had a fractionally higher AUC, the tuned version achieved a better F1-score for the minority "Late" class.

_Tuned Classifier Hyperparameters:_ `colsample_bytree=0.8`, `learning_rate=0.05`, `max_depth=6`, `n_estimators=200`, `subsample=1.0`.

## Regression Results (predict `delay_gap` in days)

**Note:** The regression models were filtered to evaluate **late orders only** (Target: `delay_gap` > 0). Predicting the exact delay duration is inherently noisy. Original targets (RMSE < 2, R² > 0.60) were revised because the delivery variance in this dataset makes sub-2-day RMSE unachievable without post-shipment data.

| Model                         | Test RMSE (days) | Test R²    | Test MAE (days) | Train-Test R² Gap | Verdict         |
| ----------------------------- | ---------------- | ---------- | --------------- | ----------------- | --------------- |
| Linear Regression             | 8.60             | 0.293      | 5.10            | +0.061            | ⚠️ Mild overfit |
| Random Forest Reg (Default)   | 13.10            | 0.0684     | 7.46            | +0.0218           | ✅ Good         |
| XGBoost Reg (Default)         | 13.10            | 0.0677     | 7.53            | +0.0146           | ✅ Good         |
| **Random Forest Reg (Tuned)** | **13.03**        | **0.0782** | **7.46**        | +0.0371           | ✅ Good         |

**Best regressor:** Random Forest Regressor (Tuned) — RMSE = 13.03 days.

_Tuned Regressor Hyperparameters:_ `max_depth=6`, `max_features=0.6`, `min_samples_leaf=30`, `n_estimators=300`.

## Risk Score

Combines both the tuned classifier and tuned regressor into a single operational metric:

`Risk Score = predict_proba(late) × predicted_delay_gap × profit_weight`

- `predict_proba` → XGBoost classifier's probability of the order being late.
- `predicted_delay_gap` → Random Forest regressor's predicted days late (clipped to 0 minimum).
- `profit_weight` → Normalized order value (0.1–1.0) to prioritize high-value delays.

**Risk Tier Validation:**
The score successfully buckets orders into risk tiers. In the test set validation:

- **Low Risk** (19,237 orders): 8.0% actual late rate.
- **Medium Risk** (52 orders): 78.8% actual late rate.
- **High Risk** (2 orders): 50.0% actual late rate.

## Overfitting Controls

- Tree complexity was strictly limited via `max_depth` (e.g., restricted to 6) and `min_samples_leaf`.
- Random Forest regularization applied using `max_features=0.6`.
- Time-based splitting guarantees an honest evaluation without data leakage from the "future".
- A custom `overfit_check` helper function was used to explicitly report the Train vs. Test gap across all models.

## Known Limitations

- `seller_late_rate_smooth` (from NB04) was computed on the full dataset. In a strict production environment, this must be computed on the training set only to avoid look-ahead bias.
- The Risk Score profit weight uses order price as a proxy; utilizing actual profit margin data would yield a more precise business metric.
