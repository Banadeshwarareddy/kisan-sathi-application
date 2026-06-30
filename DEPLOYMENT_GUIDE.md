# Kisan Sathi - Deployment Guide

## ✅ Pre-Deployment Checklist Completed

Your application is now ready for hosting! Here's what has been done:

### Security Improvements Applied:
- ✅ New SECRET_KEY generated
- ✅ DEBUG set to False (for production)
- ✅ Security headers added (SSL, HSTS, XSS protection)
- ✅ Static files collected with WhiteNoise
- ✅ .gitignore created to protect secrets

---

## 📋 Deployment Steps by Platform

### Option 1: Deploy to Render.com (Recommended - FREE)

**Why Render?**
- Free tier available
- Easy Django deployment
- Auto SSL certificates
- PostgreSQL database included

**Steps:**

1. **Create account** at https://render.com

2. **Create Web Service:**
   - Connect your GitHub repository
   - Select "Python" environment
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn kisan_sathi.wsgi:application`

3. **Add Environment Variables** in Render dashboard:
   ```
   SECRET_KEY=q@@6q6ape36xu@i&1qhpe34wdsq&+l=b1w8^nmsnkhtrnf6j+*
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   DATABASE_URL=(Render will auto-generate PostgreSQL URL)
   OPENWEATHERMAP_API_KEY=14cf7e21e3caca61975230fea391ad1f
   GROQ_API_KEY=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
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

4. **Create PostgreSQL Database** (in Render):
   - Click "New +" → "PostgreSQL"
   - Copy the "Internal Database URL"
   - Add it as `DATABASE_URL` environment variable

5. **Deploy!** Render will automatically build and deploy

---

### Option 2: Deploy to Railway.app (Easy & Fast)

1. Visit https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Add environment variables from `.env`
6. Railway will auto-detect Django and deploy

---

### Option 3: Deploy to PythonAnywhere (Simple)

1. Sign up at https://www.pythonanywhere.com
2. Upload your code via Git or zip
3. Create virtual environment: `python -m venv venv`
4. Install requirements: `pip install -r requirements.txt`
5. Configure WSGI file to point to your app
6. Add static files mapping
7. Reload web app

---

### Option 4: VPS (DigitalOcean, AWS, etc.)

**Requirements:**
- Ubuntu 20.04+ server
- Nginx web server
- Gunicorn WSGI server
- PostgreSQL database
- SSL certificate (Let's Encrypt)

**Quick Setup:**
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv postgresql nginx

# Clone your repo
git clone your-repo-url
cd stitch_kisan_sathi_smart_farming_app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt gunicorn psycopg2-binary

# Setup PostgreSQL
sudo -u postgres psql
CREATE DATABASE kisansathi;
CREATE USER kisanuser WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE kisansathi TO kisanuser;
\q

# Update .env with production values
nano .env

# Run migrations
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Test with Gunicorn
gunicorn kisan_sathi.wsgi:application --bind 0.0.0.0:8000

# Configure Nginx (create /etc/nginx/sites-available/kisansathi)
# Configure systemd service for auto-start
# Get SSL with certbot
```

---

## 🔒 Security Checklist Before Going Live

- [ ] Change admin password to something strong
- [ ] Update ALLOWED_HOSTS with your actual domain
- [ ] Ensure DEBUG=False in production
- [ ] Use PostgreSQL instead of SQLite (for better performance)
- [ ] Enable HTTPS/SSL certificate
- [ ] Set up regular database backups
- [ ] Consider hiding admin URL (change from /admin/ to something secret)
- [ ] Set up monitoring and error logging (Sentry)
- [ ] Review and secure all API keys

---

## 📦 Required Files for Deployment

Your project already has:
- ✅ `requirements.txt` - Python dependencies
- ✅ `settings.py` - Configured with environment variables
- ✅ `.env` - Environment configuration (DO NOT commit to Git!)
- ✅ `.gitignore` - Protects secrets
- ✅ WhiteNoise - Serves static files
- ✅ Trained AI model - Ready for predictions

---

## 🎯 After Deployment

1. **Test everything:**
   - Landing page
   - User registration/login
   - Dashboard
   - Crop disease detector
   - Weather features
   - Chatbot
   - Farm management

2. **Set strong admin password:**
   ```bash
   python manage.py changepassword admin
   ```

3. **Monitor logs** for any errors

4. **Setup custom domain** (optional):
   - Buy domain from Namecheap/GoDaddy
   - Point DNS to hosting provider
   - Update ALLOWED_HOSTS

---

## 🚨 Common Issues & Solutions

**Issue: Static files not loading**
- Solution: Run `python manage.py collectstatic` and check STATIC_ROOT

**Issue: Database errors**
- Solution: Run `python manage.py migrate`

**Issue: 400 Bad Request**
- Solution: Add your domain to ALLOWED_HOSTS in .env

**Issue: Admin panel not accessible**
- Solution: Ensure you've created a superuser

**Issue: HTTPS redirect errors**
- Solution: Temporarily set SSL settings to False if not using HTTPS yet

---

## 📞 Need Help?

- Django Deployment Docs: https://docs.djangoproject.com/en/stable/howto/deployment/
- Render Docs: https://render.com/docs/deploy-django
- Railway Docs: https://docs.railway.app/

---

## ⚡ Quick Deploy Commands

```bash
# Generate new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Test locally
python manage.py runserver

# Run with Gunicorn (production)
gunicorn kisan_sathi.wsgi:application --bind 0.0.0.0:8000
```

---

**Good luck with your deployment! 🚀**
