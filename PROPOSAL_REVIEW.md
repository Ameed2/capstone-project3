# Proposal review: Predicting Developer Compensation

## Proposal check

- **Problem & stakeholders:** Clear. Salary benchmarks for developers and employers; bootcamp grads, HR, instructors as stakeholders.
- **Dataset:** Stack Overflow 2025 survey; source URL and ODbL license noted. One row = one survey response. ✓
- **Track:** Supervised – Regression. Target = `ConvertedCompYearly` (USD). ✓
- **Success criteria:** R² ≥ 0.55, RMSE/MAE in USD, SHAP top 10, beat median baseline. Appropriate for regression.
- **Approach:** Cleaning → feature engineering (multi-hot, ordinal, log target) → Linear Regression baseline → Decision Tree → Random Forest / XGBoost → tuning → SHAP. Fits the capstone workflow.
- **Risks:** Self-report bias, geography skew, multi-select encoding, skew/log transform, 2025 snapshot. All noted.
- **Week plan:** Weeks 7–12 mapped to cleaning, features, baseline, advanced models, evaluation, presentation. ✓
- **Roles:** Data, Modeling, Evaluation, Presentation. ✓

**Suggestions**

1. **R² ≥ 0.55:** Salary is noisy; if you land a bit below (e.g. 0.45–0.50), still report it and discuss (feature set, country skew, outliers). Capstone values a clear process.
2. **Median baseline:** Define it explicitly (e.g. predict median salary for everyone; compute RMSE/MAE and R² on test). Your “must outperform” is then testable.
3. **Train/test split:** Use a single time-based or random split and fix it (e.g. `random_state=42`), so all model comparisons are on the same test set.
4. **Mixed types warning:** Your CSV has mixed types in some columns. When loading, use `low_memory=False` or `dtype=` for those columns to avoid silent type coercion during cleaning/EDA.

---

## Data check (head only)

Checked using the first rows of `survey_results_public.csv` only (no full-table scan).

- **Shape (full file):** 49,191 rows × 172 columns (proposal said ~65k+; your sample may be a subset or different release—still sufficient).
- **Target:** `ConvertedCompYearly` present; numeric (e.g. 61256, 104413, 53061 in head). ✓
- **Key feature columns:** All present: `YearsCode`, `WorkExp`, `Country`, `RemoteWork`, `DevType`, `ICorPM`, `EdLevel`, `LanguageHaveWorkedWith`, `DatabaseHaveWorkedWith`, `OrgSize`, `AISelect`. ✓
- **Sample values:** Country (e.g. Ukraine, Netherlands), `WorkExp`/`YearsCode` numeric, multi-select text in language/DB columns—matches planned encoding (multi-hot, ordinal). ✓

**Data note:** Loading the full CSV triggers a `DtypeWarning` for mixed types in several columns. Use `pd.read_csv(..., low_memory=False)` (or fix dtypes) in your pipeline to avoid surprises.

---

## Summary

Proposal is clear, aligned with the capstone guide, and feasible. Data (checked with head only) has the target and all listed features; you can proceed with cleaning and EDA as planned.
