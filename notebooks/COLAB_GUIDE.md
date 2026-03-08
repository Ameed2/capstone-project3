# How to use Google Colab with this project

## 1. Open Google Colab

1. Go to **https://colab.research.google.com/**
2. Sign in with your Google account.

---

## 2. Create a new notebook

**Option A: Start from scratch**
- Click **File → New notebook** (or the “+ New notebook” button).
- You get a blank notebook. Rename it: double‑click the title at the top (e.g. “Untitled.ipynb”) and type something like `capstone_main`.

**Option B: Upload a notebook from this folder**
- Click **File → Upload notebook**.
- Choose a `.ipynb` file from your `notebooks/` folder (e.g. `main.ipynb`).
- Colab opens it. You can edit and run it there.

---

## 3. Connect to Colab (runtime)

Colab runs your code on Google’s servers. You need to “connect” to start running.

- At the top right you’ll see **“Connect”** or **“Reconnect”**.
- Click **Connect**. Colab will attach a runtime (free tier is enough).
- When connected, it shows something like **“Connected”** or **“RAM / Disk”** at the top right.
- You can now run cells with **Shift+Enter** or the play button.

If it disconnects (e.g. after idle time), click **Connect** again and run your cells from the top if needed.

---

## 4. Use your dataset in Colab

**If your data is on your computer (e.g. `survey_results_public.csv`):**

1. In Colab’s left sidebar, click the **Files** icon (folder).
2. Click **Upload to session storage** (upload icon).
3. Select your file (e.g. `survey_results_public.csv`).
4. In a cell, load it:

```python
import pandas as pd
df = pd.read_csv("survey_results_public.csv")
df.head()
```

**If you want to use Google Drive:**

1. In a cell, run:
```python
from google.colab import drive
drive.mount('/content/drive')
```
2. When the prompt appears, sign in and allow access.
3. Put your file in Drive (e.g. in a folder “Capstone”). Then in Colab:
```python
df = pd.read_csv("/content/drive/MyDrive/Capstone/survey_results_public.csv")
```

---

## 5. Save your work

- **Save in Colab:** **File → Save** (saves to your Google Drive by default if you’ve set that up, or to Colab’s temporary storage).
- **Save back to your PC:** **File → Download → Download .ipynb**. Put the downloaded file in your `notebooks/` folder so your repo stays up to date.
- **Share with teammates:** **File → Share** and add their email, or copy the “Share” link.

---

## 6. Add your Colab link to the README

When you’re happy with the notebook:
1. In Colab: **File → Share**.
2. Set access to “Anyone with the link” (or as your course allows).
3. Copy the link.
4. Paste it in the **“How to run”** section of the main **README.md** so mentors and reviewers can open it.

---

## Quick checklist

- [ ] Go to colab.research.google.com and sign in  
- [ ] File → New notebook (or Upload notebook from `notebooks/`)  
- [ ] Click **Connect** at top right  
- [ ] Upload your CSV via the Files sidebar, or mount Drive  
- [ ] Use `pd.read_csv("filename.csv")` (or your Drive path)  
- [ ] Save: Download .ipynb and put it in `notebooks/`  
- [ ] Add the Colab link to README.md  
