# 🚀 Deployment Guide: Code Explainer App

This guide provides step-by-step instructions to push your code to **GitHub** and deploy it to the web.

---

## 1. Prepare for Git

First, ensure you have a `.gitignore` file so your private API keys (`.env`) are not accidentally shared.

### Create `.gitignore`
In your project root, create a file named `.gitignore` and add:
```text
.env
__pycache__/
.streamlit/
*.pyc
```

---

## 2. Push to GitHub

1. **Initialize Git**:
   ```bash
   git init
   ```

2. **Add and Commit**:
   ```bash
   git add .
   git commit -m "Initial commit: Premium Code Explainer with fallback models"
   ```

3. **Create a Repository on GitHub**:
   - Go to [github.com/new](https://github.com/new).
   - Name your repo (e.g., `code-explainer-app`).
   - Leave it public.

4. **Connect and Push**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/code-explainer-app.git
   git branch -M main
   git push -u origin main
   ```

---

## 3. Deploy to Streamlit Community Cloud (Recommended)

Streamlit's official platform is the **best and easiest** way to host this app for free.

1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Log in with GitHub.
3. Click **"New app"**.
4. Select your repository (`code-explainer-app`), branch (`main`), and main file (`app.py`).
5. **Crucial**: Click **"Advanced settings..."** before deploying.
   - In the **Secrets** box, add your API key:
     ```toml
     OPENROUTER_API_KEY = "sk-or-v1-your-key-here"
     ```
6. Click **"Deploy!"**.

---

## 4. Deploy to Vercel (Experimental)

Streamlit relies on persistent WebSocket connections, which are not natively supported by Vercel's Serverless Functions. However, you can deploy your project structure to Vercel using the provided `api/index.py` and `vercel.json` files.

### Steps to Deploy on Vercel:

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Select Settings**:
   - Set the root directory to your project folder.
   - Vercel will automatically detect the `vercel.json` and use the `@vercel/python` builder.

### Highly Recommended Alternative:
For a stable experience with Streamlit, **Streamlit Community Cloud** is the industry standard and provides the persistent server connection your app needs to function without timeouts.

---

## 🔑 Environment Variables

Regardless of the platform, **never hardcode your API key**. Always use the platform's "Secrets" or "Environment Variables" settings to provide the `OPENROUTER_API_KEY`.
