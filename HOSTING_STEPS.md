# 🚀 Kisan Sathi - Simple Hosting Guide

## Choose Your Hosting Platform (Pick ONE)

### ⭐ Option 1: Render.com (RECOMMENDED - Easiest & Free)
### ⭐ Option 2: PythonAnywhere (Simplest for Beginners)
### ⭐ Option 3: Railway.app (Fastest Deployment)

---

## 🎯 Option 1: Render.com (RECOMMENDED)

### Why Render?
- ✅ Completely FREE tier
- ✅ Auto SSL certificate (HTTPS)
- ✅ Free PostgreSQL database
- ✅ Easy GitHub integration
- ✅ Auto-deploys on code push

### Step-by-Step Guide

#### Step 1: Prepare Your Code

**1.1 Push to GitHub (if not already done)**
```bash
cd stitch_kisan_sathi_smart_farming_app

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Kisan Sathi project"

# Add GitHub remote (create repo first on GitHub.com)
git remote add origin https://github.com/YOUR_USERNAME/kisan-sathi.git

# Push
git push -u origin main
```

**1.2 Create Render Configuration File**

Create `render.yaml` in project root:
```yaml
services:
  - type: web
    name: kisan-sathi
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
    startCommand: gunicorn kisan_sathi.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
```

#### Step 2: Create Render Account

1. Go to https://render.com
2. Click **"Get Started"**
3. Sign up with GitHub (easiest option)
4. Authorize Render to access your repositories

#### Step 3: Create PostgreSQL Database

1. Click **"New +"** → **"PostgreSQL"**
2. Fill in:
   - Name: `kisan-sathi-db`
   - Database: `kisansathi`
   - User: `kisansathi`
   - Region: Choose closest to you
   - Plan: **Free**
3. Click **"Create Database"**
4. Wait 2-3 minutes for database creation
5. **Copy the "Internal Database URL"** (you'll need this)

#### Step 4: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository:
   - Click **"Connect Repository"**
   - Select `kisan-sathi` repository
3. Fill in details:
   - **Name**: `kisan-sathi`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `stitch_kisan_sathi_smart_farming_app`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**: 
     ```bash
     gunicorn kisan_sathi.wsgi:application
     ```
   - **Plan**: **Free**

4. Click **"Advanced"** to add environment variables

#### Step 5: Add Environment Variables

Click **"Add Environment Variable"** for each:

```
SECRET_KEY = q@@6q6ape36xu@i&1qhpe34wdsq&+l=b1w8^nmsnkhtrnf6j+*
DEBUG = False
ALLOWED_HOSTS = .onrender.com
DATABASE_URL = [Paste Internal Database URL from Step 3]
OPENWEATHERMAP_API_KEY = 14cf7e21e3caca61975230fea391ad1f
GROQ_API_KEY = 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
GROQ_MODEL = llama-3.3-70b-versatile
CORS_ALLOWED_ORIGINS = https://your-app-name.onrender.com
```

5. Click **"Create Web Service"**

#### Step 6: Wait for Deployment

- Render will automatically build and deploy (5-10 minutes)
- Watch the logs in real-time
- Look for: **"Your service is live 🎉"**

#### Step 7: Create Superuser

1. Go to your service dashboard
2. Click **"Shell"** tab
3. Run:
```bash
python manage.py createsuperuser
```
4. Enter username, email, password

#### Step 8: Access Your Website

Your app will be live at:
```
https://kisan-sathi.onrender.com
```

⚠️ **Important**: Free tier may "spin down" after inactivity. First load after inactivity takes 30-60 seconds.

---

## 🎯 Option 2: PythonAnywhere (Simplest)

### Why PythonAnywhere?
- ✅ Very beginner-friendly
- ✅ No Git required
- ✅ Free tier available
- ✅ Simple web interface

### Step-by-Step Guide

#### Step 1: Create Account

1. Go to https://www.pythonanywhere.com
2. Click **"Pricing & signup"**
3. Choose **"Create a Beginner account"** (FREE)
4. Fill in username, email, password
5. Verify email

#### Step 2: Upload Your Code

**Option A: Using Git (Recommended)**
1. Click **"Consoles"** → **"Bash"**
2. Run:
```bash
git clone https://github.com/YOUR_USERNAME/kisan-sathi.git
cd kisan-sathi/stitch_kisan_sathi_smart_farming_app
```

**Option B: Upload ZIP**
1. Zip your `stitch_kisan_sathi_smart_farming_app` folder
2. Click **"Files"** → **"Upload a file"**
3. Upload and extract

#### Step 3: Create Virtual Environment

In Bash console:
```bash
cd kisan-sathi/stitch_kisan_sathi_smart_farming_app
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 4: Configure Database

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

#### Step 5: Set Up Web App

1. Go to **"Web"** tab
2. Click **"Add a new web app"**
3. Choose:
   - **Manual configuration**
   - **Python 3.11**
4. Click through setup

#### Step 6: Configure WSGI File

1. In **"Web"** tab, click on WSGI configuration file
2. Delete all content and replace with:

```python
import os
import sys

# Add your project directory
path = '/home/YOUR_USERNAME/kisan-sathi/stitch_kisan_sathi_smart_farming_app'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'kisan_sathi.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

3. Save file

#### Step 7: Set Virtual Environment Path

1. In **"Web"** tab, find **"Virtualenv"** section
2. Enter path:
```
/home/YOUR_USERNAME/kisan-sathi/stitch_kisan_sathi_smart_farming_app/venv
```

#### Step 8: Set Environment Variables

1. In **"Web"** tab, scroll to **"Environment variables"**
2. Add:
```
SECRET_KEY = q@@6q6ape36xu@i&1qhpe34wdsq&+l=b1w8^nmsnkhtrnf6j+*
DEBUG = False
ALLOWED_HOSTS = .pythonanywhere.com
```

#### Step 9: Configure Static Files

1. In **"Web"** tab, find **"Static files"** section
2. Add mapping:
   - URL: `/static/`
   - Directory: `/home/YOUR_USERNAME/kisan-sathi/stitch_kisan_sathi_smart_farming_app/staticfiles/`

#### Step 10: Reload Web App

1. Click big green **"Reload"** button
2. Visit: `https://YOUR_USERNAME.pythonanywhere.com`

---

## 🎯 Option 3: Railway.app (Fastest)

### Why Railway?
- ✅ Fastest deployment (literally 5 minutes)
- ✅ Auto-detects Django
- ✅ Free $5/month credit
- ✅ GitHub integration

### Step-by-Step Guide

#### Step 1: Prepare Code

Push to GitHub (same as Render Option 1, Step 1.1)

#### Step 2: Create Railway Account

1. Go to https://railway.app
2. Click **"Login"** → **"Login with GitHub"**
3. Authorize Railway

#### Step 3: Deploy

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose `kisan-sathi` repository
4. Railway auto-detects Django
5. Click **"Deploy"**

#### Step 4: Add PostgreSQL

1. Click **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway auto-connects it to your app

#### Step 5: Add Environment Variables

1. Click on your service
2. Go to **"Variables"** tab
3. Click **"+ New Variable"** and add:

```
SECRET_KEY = q@@6q6ape36xu@i&1qhpe34wdsq&+l=b1w8^nmsnkhtrnf6j+*
DEBUG = False
ALLOWED_HOSTS = .up.railway.app
OPENWEATHERMAP_API_KEY = 14cf7e21e3caca61975230fea391ad1f
GROQ_API_KEY = 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
```

4. Railway automatically redeploys

#### Step 6: Run Migrations

1. Click on your service
2. Go to **"Settings"** → **"Deploy"**
3. Add under **"Build Command"**:
```bash
python manage.py migrate && python manage.py collectstatic --noinput
```

#### Step 7: Create Superuser

1. Click **"Settings"** → **"Shell"**
2. Run:
```bash
python manage.py createsuperuser
```

#### Step 8: Access Your App

Railway gives you a URL like:
```
https://kisan-sathi-production.up.railway.app
```

---

## 🔧 Common Issues & Fixes

### Issue 1: Static Files Not Loading

**Fix for Render/Railway:**
```bash
# Add to build command
python manage.py collectstatic --noinput
```

**Fix for PythonAnywhere:**
- Check Static files mapping in Web tab
- Ensure path is correct

### Issue 2: Database Error

**Fix:**
```bash
# Run migrations
python manage.py migrate
```

### Issue 3: 400 Bad Request

**Fix:**
- Add your domain to `ALLOWED_HOSTS` in environment variables
- Example: `.onrender.com` or `.pythonanywhere.com`

### Issue 4: 500 Internal Server Error

**Fix:**
1. Check logs in hosting dashboard
2. Ensure `DEBUG=False` in production
3. Verify all environment variables are set

### Issue 5: Admin Panel Won't Load

**Fix:**
```bash
# Create superuser
python manage.py createsuperuser
```

---

## ✅ Post-Deployment Checklist

After deployment, verify:

- [ ] Website loads at your URL
- [ ] Landing page displays correctly
- [ ] User registration works
- [ ] Login works
- [ ] Dashboard loads
- [ ] Crop detector accepts images
- [ ] AI prediction works
- [ ] Weather data loads
- [ ] Chatbot responds
- [ ] Farm management works
- [ ] Admin panel accessible at `/admin/`
- [ ] Static files (CSS, JS) loading
- [ ] Images displaying correctly

---

## 🎯 Quick Comparison

| Feature | Render | PythonAnywhere | Railway |
|---------|--------|----------------|---------|
| **Free Tier** | ✅ Yes | ✅ Yes | ✅ $5/month credit |
| **Ease of Use** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Speed** | Fast | Medium | Very Fast |
| **Database** | PostgreSQL included | SQLite only (free) | PostgreSQL extra |
| **SSL/HTTPS** | ✅ Auto | ❌ Paid only | ✅ Auto |
| **Custom Domain** | ✅ Yes | ✅ Paid | ✅ Yes |
| **Sleep Time** | After 15min inactive | No sleep | No sleep |

**Recommendation:**
- **For Portfolio/Demo**: Render.com (free, looks professional)
- **For Learning**: PythonAnywhere (simplest, no Git required)
- **For Speed**: Railway.app (deploys in 5 minutes)

---

## 🆘 Need Help?

**Render Support**: https://render.com/docs
**PythonAnywhere Help**: https://help.pythonanywhere.com
**Railway Docs**: https://docs.railway.app

**Common Commands:**

```bash
# Check if app is running
python manage.py check

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Test locally
python manage.py runserver
```

---

## 🎉 Success!

Once deployed, share your link:
```
My Kisan Sathi App: https://your-app-name.onrender.com
```

Add it to your:
- Resume
- LinkedIn
- GitHub README
- Portfolio website

**Pro Tip**: Take screenshots and record a demo video for your portfolio!

---

**Last Updated**: January 2024
