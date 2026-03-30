# Olist Delivery Delay Prediction — Notebooks

This directory contains the core Jupyter Notebooks for the Olist Delivery Delay Prediction Capstone Project. The pipeline is broken down into five sequential stages, from raw data ingestion to final predictive modeling and risk scoring.

## 📂 Notebook Pipeline

Below is the execution order of the notebooks. For detailed information on the inputs, outputs, and key decisions made in each stage, please refer to their linked README files.

- **[Notebook 01 — Data Understanding & Cleaning](./README/README_01_cleaning.md)**
  - Loads the 9 raw CSV files, handles missing values, fixes data types, and creates the baseline `is_late` target variable.
- **[Notebook 02 — Data Merging](./README/README_02_merging.md)**
  - Aggregates items, payments, and geolocation data to construct a unified, order-level dataset (`olist_merged.csv`).
- **[Notebook 03 — Exploratory Data Analysis](./README/README_03_eda.md)**
  - Explores distributions, temporal spikes, and geographic patterns to uncover signals driving late deliveries.
- **[Notebook 04 — Feature Engineering](./README/README_04_features.md)**
  - Transforms raw data into a model-ready feature matrix, including seller historical performance, bottleneck identification, and haversine distance.
- **[Notebook 05 — Supervised Modelling](./README/README_05_modelling.md)**
  - Trains and evaluates classification (predicting if an order will be late) and regression (predicting the delay gap) models, resulting in a finalized operational Risk Score.

---

**Note:** To reproduce the results, please execute the notebooks in numerical order (01 through 05), ensuring the `assets/data/raw/` directory contains the initial Olist dataset files.
