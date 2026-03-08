# GitHub setup for your capstone

Follow these steps to put your project on GitHub. You can do this before or after you change the project idea.

---

## 1. Create a new repo on GitHub

1. Go to **https://github.com/new**
2. **Repository name:** e.g. `capstone-developer-compensation` (or whatever fits your new idea)
3. **Description:** optional, e.g. "Data Science capstone – [short description]"
4. Choose **Public**
5. **Do not** check "Add a README", "Add .gitignore", or "Choose a license" (you already have these locally)
6. Click **Create repository**

---

## 2. Connect this folder to GitHub

Open a terminal in your project folder (`Capstone-project`) and run (replace with **your** username and repo name):

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

Example:
```bash
git remote add origin https://github.com/jane-doe/capstone-ml-project.git
```

---

## 3. Push your code

```bash
git branch -M main
git push -u origin main
```

If GitHub asks for login, use your GitHub username and a **Personal Access Token** (not your password).  
To create a token: GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Generate new token**.

---

## 4. After you change the project idea

When you’re ready to work on the new idea:

- Update **README.md** (title, problem, data, approach)
- Update the **notebook** (or add a new one) when you start
- Commit and push as usual:
  ```bash
  git add .
  git commit -m "Describe what you did"
  git push
  ```

---

## One submission per group

Your capstone guide says: submit **one GitHub repo link per group** by end of Week 12. Make sure everyone has access to this repo (add them as collaborators under **Settings** → **Collaborators**).
