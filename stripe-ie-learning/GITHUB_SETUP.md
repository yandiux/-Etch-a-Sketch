# Connect this folder to GitHub (one-time)

The Cloud Agent **cannot** create repos on your GitHub account (API permission). You create an empty repo; this folder is already committed and ready to push.

## Step 1 — Create empty repo on GitHub

1. Open https://github.com/new  
2. Repository name: **`stripe-ie-learning`**  
3. Visibility: **Private** (recommended)  
4. **Do not** add README, .gitignore, or license (this folder already has them)  
5. Click **Create repository**

## Step 2 — Push from your machine

If you cloned or copied this folder locally:

```bash
cd stripe-ie-learning
git remote add origin https://github.com/YOUR_USERNAME/stripe-ie-learning.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub handle (e.g. `yandiux`).

## Step 3 — Open in Cursor

File → Open Folder → `stripe-ie-learning`  
Use weekly check-ins in [docs/MENTOR-GUIDE.md](./docs/MENTOR-GUIDE.md).

## Already on `-Etch-a-Sketch`?

The same lab lives on branch `cursor/ie-learning-lab-22f2` / [PR #1](https://github.com/yandiux/-Etch-a-Sketch/pull/1). You can merge that PR **or** use this dedicated repo — pick one home base, not both.
