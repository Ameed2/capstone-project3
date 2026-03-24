# Late Delivery Risk Scoring – Brazilian E-Commerce Supply Chain

**Team members:** Ameed Aburub, Aman Abuelayyan, Ruaa Luay, Dalah Hashlamoon, Sura Sammour  
**Track:** Supervised Learning — Classification + Regression (with Clustering enrichment)  
**IBT x GGateway Data Science and Machine Learning Bootcamp | 2025**

---

## Problem and goal

Late deliveries are one of the most damaging and costly problems in e-commerce logistics — but not all late deliveries are equally damaging. A 1-day delay on a low-profit order is very different from a 10-day delay on a high-value shipment.

This project builds a **4-stage pipeline** that predicts whether an order is at risk of late delivery **before it ships**, estimates how many days late it will be, and combines both signals with financial impact into a single, actionable **Risk Score**. The goal is to give supply chain and logistics managers a proactive tool to flag high-risk orders and take corrective action (e.g. upgrade shipping, reroute, or alert the customer).

**Risk Score formula:**

> **Risk Score = predict_proba × predicted_delay_gap × profit_weight**

All three components are predicted from features known at order time — no future data is used.

- **Classification target:** `is_late` (0 = on time or early, 1 = late)
- **Regression target:** `delay_gap` (actual delivery date − estimated delivery date, in days)
- **Primary metrics:** ROC-AUC > 0.80, F1 > 0.75 on the late class; RMSE < 2 days, R² > 0.60 on delay gap
- **Success criteria:** Clear separation between low / medium / high risk orders; interpretable SHAP feature importance for the stakeholder

## Who benefits

- **Primary stakeholder:** Supply chain / logistics manager — prioritize intervention, choose smarter shipping options, reduce refunds and complaints, protect customer satisfaction.
- **Secondary:** Customer service (fewer reactive complaints), leadership (visibility into fulfillment delays by region and product category).

## Data

- **Source:** Brazilian E-Commerce Public Dataset by Olist. [Dataset (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **What one row represents:** One order line item — one product within one customer order, with its full delivery, shipping, seller, payment, and review record.
- **Size:** ~112,000 order items across 9 relational tables, merged into a single master DataFrame.
- **Key tables:** `orders`, `order_items`, `customers`, `products`, `sellers`, `payments`, `reviews`, `geolocation`, `category_translation`
- **Key engineered columns:** `is_late` (classification target), `delay_gap` (regression target, days), `profit_proxy` (price − freight), `customer_lat/lng`, `seller_lat/lng`, `has_review_text`

See `PROPOSAL.md` for the full data dictionary and column descriptions.

## Approach

The project runs four connected stages, each feeding into the next:

| Stage | Method | Input → Output | Purpose |
|---|---|---|---|
| **Stage 1** | K-Means Clustering | Order features → cluster label | Discover hidden delivery risk profiles |
| **Stage 2** | Classification (XGBoost) | Features + cluster → predict_proba | Likelihood of late delivery (0–100%) |
| **Stage 3** | Regression (Random Forest) | Features + cluster → predicted delay gap | How many days late, expected? |
| **Stage 4** | Risk Score | proba × gap × profit_weight → Risk Score | One unified, explainable business score |

---

## Data Understanding & Cleaning (Week 8 — `notebook_cleaned.ipynb`)

This notebook covers the two foundational steps before any modelling: understanding the data and cleaning it systematically.

### Step 1 – Data Dictionary

We built a complete data dictionary for all 9 source tables before writing any cleaning code. For every column we documented: business meaning, raw data type, intended cast type, and known issues (nulls, typos, encoding problems). Key findings:

- `orders` is the **central hub** linking to customers, payments, reviews, and order items via `order_id`.
- `order_items` is the **bridge table** — each row is one item in one order, joining to both `products` and `sellers`.
- `geolocation` connects to both customers and sellers via `zip_code_prefix` (first 5 digits of postal code).
- Several timestamp columns were stored as plain strings and needed datetime conversion.
- Zip code prefix columns across `customers`, `sellers`, and `geolocation` were stored as integers, losing leading zeros (e.g. `1310` instead of `"01310"`).

### Step 2 – Cleaning (table by table)

We cleaned each table in a systematic order — fix data types → handle missing values → remove duplicates → flag impossible values → treat outliers — and documented every decision with a *why*.

**City names (`customers`, `sellers`, `geolocation`)**
Many city names were inconsistent due to encoding corruption, URL-encoded characters, numeric zip codes entered by mistake, and state/country suffixes. We wrote a `clean_city()` function that detects and tags each case (ok, url_decoded, encoding_fixed, city_state_split, numeric_flagged, cleaned) and normalises whitespace and punctuation.

**`orders`**
All five timestamp columns (`order_purchase_timestamp`, `order_approved_at`, `order_delivered_carrier_date`, `order_delivered_customer_date`, `order_estimated_delivery_date`) were converted from string to datetime. Rows where delivery precedes purchase were flagged. All order statuses were kept — filtering to `delivered` only happens at modelling time.

**`customers`**
Zip code prefix cast from int64 to zero-padded 5-character string for correct geolocation joins. Primary key `customer_id` confirmed to have no duplicates.

**`order_items`**
`shipping_limit_date` converted to datetime. Zero and negative prices were flagged. Outliers on `price` were identified using the IQR rule and capped at the 99th percentile (preserves top 1% without distorting the regression target).

**`products`**
Two source columns had a typo in the original dataset (`product_name_lenght`, `product_description_lenght`) — both renamed to the correct spelling. Portuguese category names were translated to English by joining the `category_translation` lookup table (left join to keep all products). The 610 rows with a missing category were filled with `"unknown"`. Missing physical dimensions (weight, length, height, width) were imputed using the category-specific median.

**`sellers`**
Same zip code fix as customers — int to zero-padded string.

**`payments`**
No nulls or datetime columns. Outliers on `payment_value` flagged at the 99th percentile. `not_defined` payment type left as-is (labelled unknown).

**`reviews`**
`review_creation_date` and `review_answer_timestamp` converted to datetime. Review text fields (~58% and ~42% missing respectively) were not imputed — instead a binary `has_review_text` flag was created.

**`geolocation`**
Zip code prefix zero-padded as above. Coordinates were validated against Brazil's bounding box (lat: −33.8° to +5.3°, lng: −73.5° to −28.8°). Rows outside this range were flagged with an `is_impossible_coord` column rather than dropped.

### Step 3 – Building the Master DataFrame

All cleaned tables were merged into one analysis-ready master DataFrame, grain = **one row per order item**:

1. Start from `order_items_clean` (atomic unit of a transaction).
2. Left-join `orders_clean` on `order_id`.
3. Left-join `customers_clean` on `customer_id`.
4. Left-join `products_clean` on `product_id`.
5. Left-join `sellers_clean` on `seller_id`.
6. Left-join aggregated `payments_clean` and `reviews_clean` on `order_id`.

Left joins were used throughout to preserve every item, even when review or payment data was missing. A post-merge null audit documented every remaining null and the decision for each. Duplicate `(order_id, order_item_id)` pairs were checked and confirmed absent.

### Step 4 – Target Variable Engineering

Three key columns were derived on the master DataFrame:

- **`delay_gap`** = `order_delivered_customer_date − order_estimated_delivery_date` (in days). Positive = late, negative = early, NaT propagates for undelivered orders.
- **`is_late`** = 1 if `delay_gap > 0`, else 0. Classification target.
- **`profit_proxy`** = `price − freight_value`. Stand-in for profit margin (real profit is not in the dataset).

The master DataFrame was saved as `olist_master_clean.csv` for use in EDA, feature engineering, and modelling notebooks.

### Step 5 – Exploratory Data Analysis (EDA)

Initial EDA was performed inline to validate the cleaned data and surface patterns relevant to late delivery prediction:

- **Delay gap distribution** — histogram of all delivered orders, and separately for late orders only, with the median delay annotated.
- **Late rate by product category** — horizontal bar chart of the top 20 categories by late delivery rate (categories with fewer than 200 orders excluded). Categories above 10% late rate highlighted in red.
- **Order value vs. lateness** — boxplot of item price by delivery outcome, and overlapping distributions of `profit_proxy` for late vs. on-time orders.
- **Monthly volume and late rate** — dual-axis chart showing order volume (bars) and late delivery rate (line) over time to identify seasonality and trend breaks.

---

## Results

- *(To be filled after modeling)* Metric table (Recall, F1, confusion matrix, ROC-AUC for classifier; RMSE, R² for regressor).
- *(To be filled)* Key charts: feature importance (SHAP), confusion matrix, ROC curve, risk score distribution (in `figures/` or inline).

## Conclusion

- *(To be filled)* What we learned; what we would recommend or do next.

---

## How to run this project

We support **both** Google Colab and local run.

### Option A: Google Colab

**One-click open (after the repo is on GitHub):**  
Replace `YOUR_USERNAME` and `YOUR_REPO` with your GitHub username and repo name:

```
https://colab.research.google.com/github/YOUR_USERNAME/YOUR_REPO/blob/main/notebooks/main.ipynb
```

1. Open the link (or Colab → **File → Open notebook → GitHub** and paste the repo URL).
2. **Dataset:** Mount your Google Drive and point the first data-loading cell to your Olist CSV folder (e.g. `"/content/drive/MyDrive/Colab Notebooks/Olist/"`). The notebook expects the 9 standard Olist CSV files.
3. **Run:** **Runtime → Run all** (or run cells top to bottom). Use the `%pip install` cell if needed, then restart and run again.
4. **Colab guide:** See `notebooks/COLAB_GUIDE.md`.

### Option B: Local run

1. Clone the repo.
2. (Optional) `python -m venv .venv` then activate (e.g. `.venv\Scripts\activate` on Windows).
3. `pip install -r requirements.txt`
4. Download the Olist dataset from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and place all 9 CSV files in `data/` (see `data/README.md` for exact filenames).
5. From project root: `jupyter notebook notebooks/` → open `notebook_cleaned.ipynb` for data cleaning, then `main.ipynb` for the full pipeline, and run all cells top to bottom.

---

## Repo structure

```
README.md
requirements.txt
PROPOSAL.md               # Full capstone proposal (problem, data, plan, roles)
notebooks/
    notebook_cleaned.ipynb    # Week 8 — data understanding, cleaning, target engineering & EDA
    main.ipynb                # Full pipeline (EDA → modelling → risk score)
slides/                   # Final presentation
figures/                  # Exported charts
data/                     # Dataset CSVs (see data/README.md)
src/                      # Optional helper scripts
```

## Making the notebook easy to read

- Section headers in markdown so the flow is clear.
- Each cleaning and modelling decision is documented with a short *why* (decision log cells).
- Keep outputs that support the story; remove noisy prints.
- Runnable top to bottom — the data path works for both Colab and local.

---

*One submission per group. Submit the repo link by end of Week 12.*
