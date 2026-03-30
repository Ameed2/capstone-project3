# Notebook 01 — Data Understanding & Cleaning

## Purpose

Load, inspect, and clean the 9 raw CSV files from the Olist dataset. Produce reliable, analysis-ready tables for downstream merging and modeling.

## Input / Output

| | Details |
|---|--------|
| **Input** | 9 raw CSVs from `assets/data/raw/` |
| **Output** | 9 cleaned CSVs saved to `assets/data/cleaned/` |
| **Key output** | `orders_clean.csv` — 96,455 rows × 13 columns (delivered orders only) |

## What This Notebook Does

**1. Data Understanding**
- Loads all 9 tables and documents their shape, types, and relationships.
- Maps the Olist data schema (ERD) showing how tables connect via `order_id`, `customer_id`, `product_id`, and `seller_id`.

**2. Type Fixes**
- Converts all timestamp columns from `object` → `datetime64` (5 in orders, 1 in items, 2 in reviews).

**3. Missing Value Handling**
- Drops 2,980 orders with incomplete delivery timestamps (cannot compute target variable without them).
- Scope-filters to `delivered` orders only → removes 6 remaining canceled orders.
- Fills optional review comment fields with `'no_comment'`.
- Fills missing product dimensions with column medians.

**4. Target Variable Creation**
- `is_late = 1` if `order_delivered_customer_date > order_estimated_delivery_date`, else 0.
- Result: **8.1% late** (7,825 orders) vs **91.9% on-time** (88,630 orders).

**5. Impossible Values**
- Replaces 4 products with `weight = 0g` → median (700g).
- Flags 1,966 high-value items (price > mean + 3σ) — retained, not removed.
- Flags 42 geolocation rows outside Brazil's bounding box.

**6. Logical Consistency Checks**
- Flags 1,373 rows with suspicious timestamp ordering (e.g., carrier pickup before payment approval). Retained for EDA investigation.

**7. Outlier Decision**
- Orders with `delivery_days > 46` (99th percentile): 879 rows, 96.5% are confirmed late. **Retained** — these are real extreme delays the model must learn from.

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Keep only delivered orders | Cannot evaluate delay for undelivered orders |
| Retain extreme outliers | 96.5% are real late deliveries, not data errors |
| Flag (don't drop) timestamp anomalies | Likely system logging artifacts; defer to EDA |
| Create `is_late` after cleaning | Avoids NaN contamination in the target |

## Notes for Next Notebook

- Class imbalance is 11.3:1 — must be addressed during modeling.
- 1,373 flagged timestamp rows should be investigated in EDA.
- `delivery_days` created here is for EDA only — it leaks post-delivery information.
