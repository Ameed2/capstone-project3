# Notebook 02 — Data Merging

## Purpose

Combine all 9 cleaned tables into a single order-level dataset ready for EDA and modeling.

## Input / Output

| | Details |
|---|--------|
| **Input** | 9 cleaned CSVs from `assets/data/cleaned/` |
| **Output** | `olist_merged.csv` (96,455 × 38), `items_enriched.csv` (112,650 × 22), `zip_geo_centroids.csv` (~19k rows) |

## What This Notebook Does

**1. Geolocation Aggregation**
- The raw geolocation table has ~1M rows (multiple coordinates per zip code). Aggregated to one centroid (mean lat/lng) per zip prefix → 19,015 unique zip codes.
- Saved as `zip_geo_centroids.csv` for reuse in NB04.

**2. Category Translation Fix**
- Two Portuguese product categories were missing from the translation table. Added manual English translations before joining.

**3. Items Enrichment**
- Joined items with products, translations, and seller info → `items_enriched.csv` (item-level, used for seller and category analysis in EDA).

**4. Order-Level Aggregation**
- Aggregated items per order: total price, total freight, total weight, total volume, item count, seller count, category count.
- Aggregated payments per order: total payment value, installments, dominant payment type (mode).
- Deduplicated reviews: kept the most recent review per order (551 orders had multiple reviews).

**5. Final Merge**
- Anchored all joins to the `orders` table using LEFT JOINs → preserves all 96,455 delivered orders.
- Join map: orders ← customers ← items_agg ← payments_agg ← reviews_slim ← customer_geo.

**6. Post-Merge Cleanup**
- Added `has_review` flag (review score is NaN for ~3% of orders — absence is informative).
- Filled remaining missing values: item columns → median, payment columns → 0/unknown.
- Dropped zero-variance column (`order_status` = always "delivered").

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Aggregate items via `sum`/`max`, not pick one | Preserves information for multi-item orders |
| Use `mode()` for payment type | A customer paying 90% credit card + 10% voucher is correctly labeled "credit card" |
| Defer seller geo to NB04 | Multi-seller orders need a "bottleneck seller" concept (defined in feature engineering) |
| Keep most recent review per order | Multiple reviews for the same order are rare (551 cases); most recent reflects final sentiment |

## Output Schema (olist_merged.csv)

38 columns covering: order timestamps, delivery flags, customer location, aggregated item features (price, freight, weight, volume, counts), payment info, review score, and customer lat/lng.
