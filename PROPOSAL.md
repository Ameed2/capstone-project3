# CAPSTONE PROJECT PROPOSAL  
# Late Delivery Risk Prediction for E-Commerce Supply Chain Optimization

**IBT x GGateway Data Science and Machine Learning Bootcamp | 2025**

| | |
|---|---|
| **Track** | Supervised Learning — **Classification + Regression** |
| **Primary Stakeholder** | Supply Chain / Logistics Manager |
| **Primary Metrics** | Recall (late class) + F1; RMSE/R² (delay magnitude); **Risk Score** (prioritization) |
| **Targets** | `Late_delivery_risk` (0/1), `Delay_Gap` (real − scheduled days) |
| **Deliverable** | Classifier + regressor combined into an actionable **Risk Score** |
| **Optional Extra** | Power BI dashboard (post-core completion only) |

---

## 1. Problem Statement

Late deliveries are one of the most damaging and costly problems in e-commerce logistics. Every delayed shipment erodes customer trust, increases operational costs through complaints and refunds, and strains relationships between retailers and their fulfillment partners. Despite having rich order and shipping data, most logistics teams react to delays after they happen — when it is already too late to intervene.

This project builds **two linked models**: (1) a **binary classifier** that predicts whether an order will be late, and (2) a **regressor** that predicts *by how many days* (delay gap). We combine them into a single **Risk Score** (e.g. P(late) × severity of predicted delay) so the manager can prioritize the worst cases first. Features include shipping mode, the gap between scheduled and real shipping days, order region, product category, customer segment, and market. The model enables a supply chain logistics manager to proactively flag high-risk orders and take corrective action — such as upgrading the shipping method, rerouting an order, or alerting the customer early.

Success means delivering a classifier and regressor that achieve strong recall and sensible delay predictions on the held-out test set, plus an interpretable **Risk Score** and feature importance that a logistics manager can act on in day-to-day operations.

---

## 2. Why It Matters & Who Benefits

The primary stakeholder is the supply chain / logistics manager at an e-commerce company. Today, they have no systematic way to identify which orders are likely to be delayed before those orders leave the warehouse. A working predictive model gives them a proactive daily tool to:

- Prioritize intervention on orders most likely to be delayed
- Select smarter shipping modes for high-risk order profiles
- Reduce the operational cost of refunds, re-shipments, and complaints
- Protect customer satisfaction and retention at scale

Secondary beneficiaries include customer service teams (fewer reactive complaints to handle) and business leadership (better visibility into fulfillment performance by region and product category).

---

## 3. Dataset

### 3.1 Source & Description

The dataset is a real-world e-commerce supply chain dataset containing order, shipping, customer, and product information. It covers multiple markets and regions globally and includes both transactional and operational data.

Each row represents a single order line item — one product within one customer order, associated with a specific delivery and shipping record.

### 3.2 Key Columns Used

| Column | Type | Role in Project |
|--------|------|-----------------|
| Late_delivery_risk | Binary (0/1) | Classification target — predict this |
| Delay_Gap | Numeric (derived) | Regression target — real days − scheduled days; built in cleaning |
| Days for shipping (real) | Numeric | Actual days taken to ship |
| Days for shipment (scheduled) | Numeric | Planned shipping days |
| Shipping Mode | Categorical | Key feature — mode of delivery |
| Delivery Status | Categorical | Delivered, late, cancelled |
| Order Region / Market | Categorical | Geographic risk signal |
| Customer Segment | Categorical | Consumer, corporate, home office |
| Category Name | Categorical | Product category |
| Order Item Discount Rate | Numeric | Discount applied to order |
| Benefit per order | Numeric | Profitability signal |
| Order Status | Categorical | Processing, shipped, complete |
| order date (DateOrders) | DateTime | Temporal feature for seasonality |

### 3.3 Dataset Checklist

- Each row represents one order line item — clearly understood
- Column meanings are documented and interpretable
- A clear classification goal is defined using an existing binary column
- Dataset is manageable in size for notebook-based analysis
- Data is from a reputable, publicly available source — safe to share
- A baseline model can realistically be built within Week 9

---

## 4. Planned Approach

### 4.1 Core Workflow

- Data loading, initial inspection, and data dictionary creation
- Data cleaning: fix type issues, handle missing values, remove duplicates, derive **Delay_Gap** (regression target)
- Exploratory Data Analysis (EDA): distributions of delay gap and late rate by region/mode/segment
- Feature engineering: encode categoricals, single feature matrix for both classifier and regressor; exclude leakage (e.g. Delivery Status)
- **Dual baselines:** Logistic Regression (classification) and Ridge (regression) with shared train/test split
- **Risk score:** combine P(late) and predicted delay into one prioritization score
- Improved models: Random Forest for classification and regression; optional GridSearchCV
- Evaluation: comparison table — Recall, F1, ROC-AUC (classification) and RMSE, R² (regression)
- Interpretation: Feature importance for both models to explain what drives late risk and delay magnitude

### 4.2 Success Criteria

- **Classification:** **Recall** on the late-delivery class **≥ 75%** and **F1 ≥ 70%** on the held-out test set
- **Regression:** Report **RMSE** and **R²** for predicted delay (Delay_Gap) on the test set
- **Risk score:** Deliver an actionable score (e.g. P(late) × (1 + max(0, predicted delay))) so the manager can prioritize orders
- Feature importance for both the classifier and the regressor is interpretable and actionable for a logistics manager

A clean, complete workflow with honest evaluation matters more than chasing the highest possible score. We will not tune on the test set.

### 4.3 Risks & Constraints

- **Class imbalance:** use `class_weight='balanced'` and evaluate with Recall/F1 rather than accuracy
- **Data leakage:** exclude columns that logically encode the outcome (e.g. Delivery Status) from features
- **Feature selection:** rely on EDA and domain reasoning to avoid noise features
- **Scope:** complete the core model before considering the Power BI dashboard extra

---

## 5. Week-Wise Plan

| Week | Focus | Key Tasks |
|------|--------|-----------|
| Week 7 | Start & Plan | Finalize dataset and confirm column roles. Set up GitHub repo and file structure. Assign team roles. Write this proposal. Align with mentor on scope and approach. |
| Week 8 | Data Setup & Cleaning | Load data and confirm quality. Build data dictionary in notebook. Clean type issues, missing values, and duplicates. First distribution charts and basic insights. Document all assumptions. |
| Week 9 | EDA & Baseline | Deepen EDA: shipping mode vs. delay, region vs. delay, segment vs. delay. Build Logistic Regression baseline with train/test split. Record baseline Recall, F1, and confusion matrix. |
| Week 10 | Improve & Compare | Train Random Forest model. Tune hyperparameters. Compare all models fairly in a results table. Check for leakage. Ask mentor for feedback on evaluation approach. |
| Week 11 | Storytelling & Draft | Select final model. Create clean charts (feature importance, confusion matrix, ROC curve). Draft README. Draft slides. Practice story. Get mentor feedback on clarity. |
| Week 12 | Polish & Submit | Final notebook cleanup — runs top to bottom. Finalize README and slides. Add Power BI dashboard if core is complete. Rehearse as a team. Submit repo link. |

---

## 6. Team Roles

| Role | Owner | Responsibilities |
|------|--------|------------------|
| Project Coordinator | TBD | Keeps weekly plan on track, runs team meetings, liaises with mentor |
| Data Lead | TBD | Data loading, cleaning, data dictionary, handles missing values |
| EDA & Visuals Lead | TBD | Distribution plots, relationship charts, storytelling visuals |
| Modeling Lead | TBD | Baseline and improved models, metric tracking, comparison table |
| Documentation Lead | TBD | README, repo organization, notebook clarity |
| Slides Lead | TBD | Presentation deck, slide flow, rehearsal coordination |
| GitHub Lead | TBD | Repo structure, commits, keeps repo clean and submission-ready |

*One team member may hold more than one role depending on team size. Roles will be finalized in Week 7.*

---

## 7. Optional Extra: Power BI Dashboard

If the core project (data cleaning, EDA, baseline model, improved model, evaluation, README, and slides) is fully completed and submitted by end of Week 11, the team will build a Power BI dashboard as an optional extra in Week 12.

The dashboard will surface:

- High-risk orders flagged by the model, filterable by region and shipping mode
- Delay rate breakdown by Market, Order Region, and Customer Segment
- Shipping mode performance comparison (late vs. on-time rates)
- Model output summary: overall Recall, F1, and confusion matrix visualization

This extra is conditional on core completion. We will not sacrifice the core project for this enhancement.
