# Late Delivery Risk Prediction for E-Commerce Supply Chain Optimization

**Team members:** Ameed Aburub, Aman Abuelayyan, Ruaa Luay, Dalah Hashlamoon, Sura Sammour  
**Track:** Supervised Learning — Binary Classification  
**IBT x GGateway Data Science and Machine Learning Bootcamp | 2025**

---

## Problem and goal

Late deliveries are one of the most damaging and costly problems in e-commerce logistics. This project builds a **binary classification model** that predicts whether an order is at risk of late delivery **before it ships**, using order and shipping data. The goal is to give supply chain / logistics managers a proactive tool to flag high-risk orders and take corrective action (e.g. upgrade shipping, reroute, or alert the customer).

- **Target variable:** `Late_delivery_risk` (0 = on time, 1 = late)
- **Primary metrics:** Recall on the late-delivery class (minimize missed high-risk orders) and F1-score
- **Success criteria:** Recall ≥ 75%, F1 ≥ 70% on the held-out test set; interpretable feature importance for the stakeholder

## Who benefits

- **Primary stakeholder:** Supply chain / logistics manager — prioritize intervention, choose smarter shipping modes, reduce refunds and complaints, protect customer satisfaction.
- **Secondary:** Customer service (fewer reactive complaints), leadership (visibility into fulfillment by region and category).

## Data

- **Source:** E-commerce supply chain dataset (order, shipping, customer, product information). [Dataset (Mendeley)](https://data.mendeley.com/datasets/8gx2fvg2k6/1)
- **What one row represents:** One order line item — one product within one customer order, with its delivery and shipping record.
- **Key columns:** `Late_delivery_risk` (target), `Days for shipping (real)`, `Days for shipment (scheduled)`, `Shipping Mode`, `Order Region`, `Market`, `Customer Segment`, `Category Name`, discount/benefit/order status/date, etc. See `PROPOSAL.md` for the full data dictionary.

## Approach

1. **Data loading & cleaning** — Load data, fix types, handle missing values, remove duplicates, treat outliers.
2. **EDA** — Distributions, late vs on-time by shipping mode / region / segment.
3. **Feature engineering** — Encode categoricals, derive delay gap (real − scheduled days), scale as needed.
4. **Baseline** — Logistic Regression with train/test split and `class_weight='balanced'` if imbalanced.
5. **Improved models** — Random Forest, then hyperparameter tuning (e.g. GridSearchCV).
6. **Evaluation** — Recall, F1, confusion matrix, ROC-AUC in a comparison table.
7. **Interpretation** — Feature importance so a logistics manager can act on the model.

We avoid data leakage (e.g. do not use `Delivery Status` as a feature when it encodes the outcome). Optional extra: Power BI dashboard after core completion (see `PROPOSAL.md`).

## Results

- *(To be filled after modeling)* Metric table (Recall, F1, confusion matrix, ROC-AUC).
- *(To be filled)* Key charts: feature importance, confusion matrix, ROC curve (in `figures/` or inline).

## Conclusion

- *(To be filled)* What we learned; what we would recommend or do next.

---

## How to run this project

We support **both** Google Colab and local run.

### Option A: Google Colab

**One-click open (after the repo is on GitHub):**  
Replace `YOUR_USERNAME` and `YOUR_REPO` with your GitHub username and repo name (use `master` instead of `main` if your default branch is `master`):

```
https://colab.research.google.com/github/YOUR_USERNAME/YOUR_REPO/blob/main/notebooks/main.ipynb
```

1. Open the link (or Colab → **File → Open notebook → GitHub** and paste repo URL).
2. **Dataset:** Upload your CSV via **Files (left sidebar) → Upload**, or mount Drive and read from there. Set the path in the first data-loading cell (e.g. `"/content/your_file.csv"` or path in `data/`).
3. **Run:** **Runtime → Run all** (or run cells top to bottom). Use the `%pip install` cell if needed, then restart and run again.
4. **Colab guide:** See `notebooks/COLAB_GUIDE.md`.

### Option B: Local run

1. Clone the repo.
2. (Optional) `python -m venv .venv` then activate (e.g. `.venv\Scripts\activate` on Windows).
3. `pip install -r requirements.txt`
4. Put the dataset in `data/` (e.g. `data/supply_chain.csv`). See `data/README.md` for source and naming.
5. From project root: `jupyter notebook notebooks/` → open `main.ipynb` and run all cells top to bottom.

---

## Repo structure

```
README.md
requirements.txt
PROPOSAL.md          # Full capstone proposal (problem, data, plan, roles)
notebooks/           # main.ipynb = main analysis
slides/              # Final presentation
figures/             # Exported charts (optional)
data/                # Dataset (see data/README.md)
src/                 # Optional scripts
```

## Making the notebook easy to read

- Section headers in markdown so the flow is clear.
- Short explanations (1–3 sentences) for important decisions.
- Keep outputs that support the story; remove noisy prints.
- Runnable top to bottom (data path works for Colab and local).

---

*One submission per group. Submit the repo link by end of Week 12.*
