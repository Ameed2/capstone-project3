# [Your Capstone Project Title]

**Team members:** [Names]  
**Track:** [Supervised / Unsupervised / Time series]

---

## Problem and goal

- What are you trying to solve or discover?
- Why does it matter? Who is the stakeholder?

## Data

- **Source:** [Link to dataset]
- **What one row represents:** [e.g. one customer, one day, one transaction]
- **Limitations or notes:** [optional]

## Approach

- Cleaning, EDA, modeling, evaluation (short summary).

## Results

- Metric table or key evaluation results.
- 2–4 key charts (can go in `figures/` or inline).

## Conclusion

- What did you learn?
- What would you recommend or do next?

## How to run this project

**Pick one option and use it consistently.**

### Option A: Google Colab (recommended for teams)

1. **Upload your notebook**  
   - Put your main notebook in `notebooks/` (e.g. `notebooks/main.ipynb`).  
   - Open [Google Colab](https://colab.research.google.com/), then **File → Upload notebook** and choose your `.ipynb` from this repo (after cloning or downloading).

2. **Dataset in Colab**  
   - **Small dataset:** In Colab, use **Files (left sidebar) → Upload** and upload your CSV/file. In the notebook, read it with the path Colab shows (e.g. `"/content/your_file.csv"`).  
   - **From Google Drive:** Mount Drive and read from your Drive path:
     ```python
     from google.colab import drive
     drive.mount('/content/drive')
     # e.g. df = pd.read_csv('/content/drive/MyDrive/your_folder/your_file.csv')
     ```
   - **From a URL:** If the dataset has a direct download link:
     ```python
     import pandas as pd
     url = "https://your-dataset-url/your_file.csv"
     df = pd.read_csv(url)
     ```

3. **Share with the team**  
   - In Colab: **File → Share** and add your group.  
   - For submission: **File → Save a copy to GitHub** (if connected) or download the notebook and add it to this repo.  
   - In this README, add: **"Main notebook (Colab): [paste Colab link here]"**.

### Option B: Local run

1. **Clone the repo** (or download and unzip).
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # Mac/Linux
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Dataset:**  
   - Place your dataset in the `data/` folder (e.g. `data/your_dataset.csv`).  
   - If the dataset is large or from Kaggle, add download steps in this README and tell readers to save the file into `data/`.
5. **Run the notebook:**  
   - From the project root: `jupyter notebook notebooks/`  
   - Open your main notebook and run top to bottom.  
   - In the notebook, load data with `../data/your_file.csv` or `./data/your_file.csv` depending on your working directory.

## Repo structure

```
README.md
requirements.txt
notebooks/       # Your Jupyter notebooks
slides/          # Final presentation slides
figures/         # Optional: exported charts
data/            # Dataset (if small) or see data/README.md
```

## Limitations and ethics (optional)

- Bias risks, privacy notes, limitations, responsible use.

---

*One submission per group. Submit the repo link by end of Week 12.*
