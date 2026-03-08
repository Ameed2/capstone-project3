# Data folder

**Do not commit large or private datasets to GitHub.**

- If your dataset is **small and allowed**: place the file(s) here (e.g. `your_dataset.csv`).
- If your dataset is **large or from Kaggle/etc.**: keep this folder empty in the repo. In your main README, add:
  - Link to download the dataset
  - Short steps to download it and where to save it (e.g. "Save as `data/your_dataset.csv`")
- Add a small sample file only if the source allows it, for others to run a quick test.

Update the path in your notebook to read from `../data/` (when running from `notebooks/`) or `./data/` as needed.
