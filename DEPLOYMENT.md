# Deployment Guide: Streamlit Community Cloud

This guide explains how to deploy the Mental Health Risk Assessment Model to **Streamlit Community Cloud**.

## Prerequisites

1. **GitHub Account** — Community Cloud deploys from GitHub repos
2. **Streamlit Account** — Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Git** — To push your code to GitHub

## Step 1: Push Your Project to GitHub

If you haven't already, initialize a Git repo and push to GitHub:

```bash
cd e:\DEPI\Technical\final\Final_project
git init
git add .
git commit -m "Initial commit: Mental Health ML model with Streamlit app"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/Final_project.git
git push -u origin main
```

Replace `<YOUR_USERNAME>` with your actual GitHub username.

## Step 2: Ensure `requirements.txt` is in the Repository Root

Check that `requirements.txt` exists in the project root (`e:\DEPI\Technical\final\Final_project\requirements.txt`):

```
streamlit
joblib
pandas
numpy
scikit-learn
```

*Note:* Add `scikit-learn` to requirements.txt if not already there (used by the model).

## Step 3: Organize App Files for Deployment

Streamlit Community Cloud expects the Streamlit script in the **repository root** or in a dedicated `app` folder. Currently, your app is at:
```
website/frontend/streamlit_test_app.py
```

**Option A (Recommended):** Copy/move the app to the repo root for easier discovery:

```bash
cp website/frontend/streamlit_test_app.py app.py
```

Then update the relative paths in `app.py` to point to `saved_models/`:

- Change: `os.path.join(os.path.dirname(__file__), '..', '..', 'saved_models')`
- To: `os.path.join(os.path.dirname(__file__), 'saved_models')`

**Option B:** Keep the app in `website/frontend/` and reference it during deployment.

## Step 4: Ensure Saved Models Are Committed to Git

The `saved_models/` folder must be in your Git repository (models are ~100MB):

```bash
git add saved_models/
git commit -m "Add trained ML models"
git push
```

*Note:* If models are too large (>100MB), consider uploading to cloud storage (AWS S3, Google Cloud Storage) instead and downloading at runtime. For now, assume they fit.

## Step 5: Deploy via Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.

2. Click **"Create app"** (top right).

3. Fill in the deployment form:
   - **GitHub repo**: `<YOUR_USERNAME>/Final_project`
   - **Branch**: `main`
   - **Main file path**: 
     - If you used Option A: `app.py`
     - If you used Option B: `website/frontend/streamlit_test_app.py`

4. Click **"Deploy"** and wait (2-5 minutes).

5. Your app will be live at a URL like: `https://final-project-<random-id>.streamlit.app`

## Step 6: Test the Deployed App

Once deployment completes:
- Navigate to the live URL
- Test the prediction form with sample data
- Verify the model loads correctly and makes predictions

## Troubleshooting

### Model Loading Error
If you see "Could not load the model", ensure:
- `saved_models/full_pipeline.pkl`, `preprocessor.pkl`, and `feature_importance.csv` are in the repo
- Paths in `streamlit_test_app.py` are correct relative to where `app.py` runs

### Large File Errors
If Streamlit Cloud rejects your app due to model size:
- Split models into smaller pickle files
- Or use cloud storage (S3/GCS) to serve models at runtime

### Python 3.14 Issues
Streamlit Community Cloud may use Python 3.12 or 3.13. Ensure `requirements.txt` works with those versions. If you have Python 3.14-specific code, update it for compatibility.

## Continuous Deployment

After your first deployment:
- Any push to `main` branch on GitHub automatically redeploys
- No manual action needed
- Rollback by reverting the commit and pushing again

## Example Deployment Checklist

- [ ] `requirements.txt` in repo root with all dependencies
- [ ] `app.py` (or `website/frontend/streamlit_test_app.py`) in repo
- [ ] `saved_models/` folder committed to Git
- [ ] All paths in app use relative paths (not absolute Windows paths)
- [ ] GitHub repo is public (or you've granted Streamlit access to private repos)
- [ ] Streamlit account created and linked to GitHub

## Next Steps

After deployment:
- Share the live URL with stakeholders
- Monitor app performance in Streamlit Cloud dashboard
- Update the app by pushing commits to `main`
- Consider adding authentication or usage limits if needed

---

**Questions?** Refer to [Streamlit Community Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
