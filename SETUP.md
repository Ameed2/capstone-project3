# Quick setup guide

## Do we use Colab or local?

**Both are allowed.** The capstone guide says:

- **Option A: Google Colab** — Use Colab for your notebooks and add a Colab link in the README.
- **Option B: Local** — Use `requirements.txt` and run notebooks on your machine.

You can use **Colab** for teamwork (easy sharing, no install) and still keep code in this repo. Many groups use Colab and upload the final notebook here.

---

## If you use Google Colab

1. Create your notebook in `notebooks/` (e.g. `main.ipynb`) or upload it to Colab first and later copy it into `notebooks/`.
2. **Dataset:**
   - **Small file:** In Colab: left sidebar → **Files** → **Upload** → choose your file. In the notebook: `pd.read_csv("/content/uploaded_filename.csv")`.
   - **In this folder on your PC:** Upload that file to Colab when you open the notebook, or put a copy in Google Drive and mount Drive in Colab, then read from Drive.
   - **From URL:** If the dataset has a direct link: `pd.read_csv("https://...")`.
3. When done, download the notebook from Colab (File → Download .ipynb) and put it in `notebooks/`. Add the Colab link to the README so reviewers can open it.

---

## If you use local (this folder on your PC)

1. Put your dataset inside **`data/`** in this folder, e.g.  
   `Capstone-project\data\your_dataset.csv`
2. Install dependencies:
   ```bash
   cd "C:\Users\hp\Desktop\Capstone-project"
   pip install -r requirements.txt
   ```
3. Start Jupyter:
   ```bash
   jupyter notebook notebooks/
   ```
4. In your notebook, load data with:
   ```python
   import pandas as pd
   df = pd.read_csv("../data/your_dataset.csv")
   ```
   (from `notebooks/`, `../data/` points to the `data` folder.)

---

## Dataset in this folder

- **Yes, you can keep the dataset inside this folder** in the `data/` subfolder.
- **Do not push large or private data to GitHub.** If the file is small and shareable, you can commit it. If it’s large or from Kaggle, keep `data/` empty in the repo and document in the README where to download the data and that it should be placed in `data/`.

---

## Summary

| Question              | Answer                                                                 |
|-----------------------|------------------------------------------------------------------------|
| Colab or local?       | Either. Colab is fine; document in README (Colab link or local steps). |
| Where does data go?   | In this folder: `data/` (e.g. `data/my_dataset.csv`).                  |
| Large dataset?        | Don’t commit it. Put link + instructions in README; others put file in `data/`. |

After you choose Colab or local, update the **How to run** section in `README.md` so anyone (and your mentor) can run the project the same way.
