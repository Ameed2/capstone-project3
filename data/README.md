# Data folder

**Do not commit large or private datasets to GitHub.**

## This project: E-commerce supply chain dataset

- **What one row is:** One order line item (one product in one customer order, with shipping/delivery record).
- **Target:** `Late_delivery_risk` (0 = on time, 1 = late).
- **Key columns:** See `PROPOSAL.md` (Section 3.2) for the full list (e.g. Days for shipping (real), Days for shipment (scheduled), Shipping Mode, Order Region, Market, Customer Segment, Category Name, etc.).

### Where to get the data

- Add here the **link** to the dataset (e.g. Kaggle, UCI, or course-provided URL) once confirmed.
- If the dataset is **small and allowed**: place the file in this folder (e.g. `data/supply_chain.csv` or the name provided by the source).
- If **large or from Kaggle**: keep this folder empty in the repo. In the main **README**, add:
  - The download link
  - Short steps (e.g. "Download from [https://data.mendeley.com/datasets/8gx2fvg2k6/1], save as `data/supple_chain.csv`")

### Using the data in the notebook

- **Local:** From project root, use `data/your_file.csv`. From `notebooks/`, use `../data/your_file.csv`.
- **Colab:** Upload the CSV to session storage (or mount Drive) and set the path in the first data-loading cell (e.g. `"/content/supply_chain.csv"`).
