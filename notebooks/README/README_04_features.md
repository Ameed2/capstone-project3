# Notebook 04 — Feature Engineering

## Purpose

Transform the merged order-level dataset into a model-ready feature matrix. Every feature decision is traced back to an EDA finding from NB03.

## Input / Output

| | Details |
|---|--------|
| **Input** | `olist_merged.csv` (96,455 × 38), `items_enriched.csv` (112,650 × 22) |
| **Output** | `olist_features.csv` (~55 columns, supervised modeling), `olist_features_cluster.csv` (~45 columns, clustering variant) |

## Features Engineered

### Step 1 — Seller Features
- **Bottleneck seller:** The seller with the latest `shipping_limit_date` per order — the rate-limiting factor in multi-seller orders.
- **Seller historical late rate:** Bayesian-smoothed to prevent small-sample sellers from having unstable extreme rates.
- **Seller order count:** Volume proxy for seller reliability.

### Step 2 — Seller-Customer Distance
- Aggregated geolocation to one centroid per zip code prefix.
- Computed **haversine distance** (km) between bottleneck seller and customer coordinates.
- Driven by EDA finding: geography is the strongest delay signal.

### Step 3 — Seller Performance Attachment
- Joined seller late rate and order count onto the order-level dataset via the bottleneck seller.

### Step 4 — Product Category Flags
- **6 grouped flags** (`has_cat_group_*`): broad groups for clustering and interpretability.
- **Dominant category:** Single most frequent category per order — for tree models.
- Avoided full one-hot encoding of all 71 categories (too sparse).

### Step 5 — Temporal Features
- Purchase month, day-of-week, hour-of-day.
- Hour bucketed into periods: early_morning, morning, afternoon, evening, night.
- Weekend flag.

### Step 6 — Logistics Timing Features
- `approval_delay_h`: Hours from purchase to payment approval.
- `carrier_handling_days`: Days from approval to carrier handoff.
- `estimated_delivery_buffer_days`: Days from purchase to estimated delivery (how generous the promise window is).
- `shipping_limit_proximity_days`: How close the latest shipping limit is to the estimated delivery date.

### Step 7 — Log Transformations
- Applied to `total_price`, `total_freight`, `total_weight_g`, `total_volume_cm3` to reduce right-skew.

### Step 8 — Categorical Encoding
- Label-encoded: `customer_state`, `bottleneck_seller_state`, `payment_type`, `dominant_category_group`, `purchase_hour_bucket`.

### Step 9 — Leakage Removal
- Dropped all post-delivery columns: `delivery_days`, `delivery_status`, `review_score`, `order_delivered_customer_date`, and all raw timestamps (replaced by engineered deltas).

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Bottleneck seller = max shipping limit | Identifies the rate-limiting seller in multi-seller orders |
| Bayesian smoothing for seller late rate | Prevents 1-order sellers from having 0% or 100% rates |
| Haversine over Euclidean distance | Accounts for Earth's curvature on Brazil-scale distances |
| Grouped category flags over full OHE | 71 dummies would be too sparse; grouped flags are interpretable |
| Two output files | Supervised file includes target-encoded features; clustering file excludes them |

## Final Feature Matrix

- **Rows:** 96,455 (one per delivered order)
- **Columns:** ~55 (49 numeric + 5 categorical, label-encoded)
- **Target:** `is_late` (binary, 8.1% positive)
