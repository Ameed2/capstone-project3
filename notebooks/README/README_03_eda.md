# Notebook 03 — Exploratory Data Analysis

## Purpose

Understand distributions, relationships, and patterns related to late delivery. Surface findings that drive feature engineering and modeling decisions.

## Input / Output

| | Details |
|---|--------|
| **Input** | `olist_merged.csv` (96,455 × 38), `items_enriched.csv` (112,650 × 22) |
| **Output** | EDA findings → documented decisions for NB04 and NB05 |

## Key Findings

### 1. Target Variable
- **8.1% late** vs 91.9% on-time (11:1 imbalance). A naive "always on-time" model hits ~92% accuracy → must use F1 and ROC-AUC instead.

### 2. Distributions
- `delivery_days` is right-skewed with a long tail (median 10 days, 99th percentile 46 days, max 209 days).
- Price and freight are heavily right-skewed → log transformation recommended.
- Most orders contain a single item; multi-item orders are uncommon.
- Review scores follow a J-shaped distribution (5-star dominant, then 1-star).

### 3. Relationships with Target
- **Physical features:** Late orders have higher freight, greater weight, and larger volume. Makes physical sense — heavier/bulkier items are harder to ship on time.
- **Multi-item orders:** Higher late rate due to more sellers and logistics complexity.
- **Review scores:** Strong inverse relationship (late → 1–2 stars). But review scores are post-delivery and cannot be model features.

### 4. Temporal Patterns
- Monthly late rate spikes during Black Friday and holiday season (logistics capacity strain).
- Day-of-week: modest variation; weekend orders face slight delays.
- Hour-of-day: late-night orders (midnight–6 AM) have the highest late rates (~9%); mid-morning orders have the lowest (~5.4%).

### 5. Geographic Patterns
- **Strongest signal in the dataset.** North and Northeast states show 2–3× the late rate of Southeastern states.
- Most sellers are concentrated in São Paulo — physical distance to remote customers drives delays.
- Implication: seller-to-customer haversine distance should be a top feature.

### 6. Product Categories
- Categories with highest late rates (furniture, home appliances) also have the heaviest weights and largest volumes.
- Product category encodes physical shipping difficulty, but weight/volume already capture most of this signal numerically.

### 7. Seller Analysis
- Seller late rates vary enormously (0% to 40%+).
- High-volume sellers converge toward the average; low-volume sellers show extreme variance.
- Seller historical performance carries real predictive signal.

### 8. Correlation Analysis
- Individual linear correlations with `is_late` are weak (< 0.15) — expected for a non-linear problem.
- Multicollinearity clusters: `total_price ↔ total_payment_value`, `weight ↔ volume ↔ freight`, `n_items ↔ n_sellers`.
- Weak linear correlations suggest tree-based models will outperform linear ones.

## Decisions Driven by EDA

| Finding | Action in NB04/NB05 |
|---------|---------------------|
| Geography is the strongest signal | Engineer haversine distance (seller → customer) |
| Physical features matter | Include weight, volume, freight; apply log transforms |
| Seller performance varies widely | Compute seller historical late rate with Bayesian smoothing |
| Temporal spikes exist | Extract purchase month, day-of-week, hour bucket |
| Class imbalance at 11:1 | Use balanced class weights; evaluate with F1/AUC |
| Weak linear correlations | Prioritize tree-based models (Random Forest, XGBoost) |
