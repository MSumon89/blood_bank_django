# Deployment Guide - Blood Management System

## 🚀 Quick Deployment to Popular Platforms

This guide covers deploying your Blood Management System to production servers.

---

## 📋 Pre-Deployment Checklist

- [ ] All features tested locally
- [ ] Sample data works correctly
- [ ] No console errors
- [ ] Forms validate properly
- [ ] Responsive design verified
- [ ] Screenshots taken
- [ ] README updated
- [ ] requirements.txt generated
- [ ] Environment variables identified
- [ ] Database migrations applied

---

## 🔧 Prepare for Deployment

### 1. Update settings.py

Create a `production_settings.py` or use environment variables:

```python
import os
from decouple import config

# Security
SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email (Production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 2. Install Additional Dependencies

```bash
pip install gunicorn whitenoise psycopg2-binary python-decouple
pip freeze > requirements.txt
```

### 3. Create .env file (DO NOT commit to git)

```env
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=blood_management_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 4. Update Middleware for Whitenoise

In `settings.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... rest of middleware
]
```

---

## 🌐 Deploy to Render.com (Recommended)

### Step 1: Prepare Files

Create `build.sh`:
```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_sample_data
```

Make it executable:
```bash
chmod +x build.sh
```

Create `render.yaml`:
```yaml
databases:
  - name: blood_management_db
    databaseName: blood_management
    user: blood_user

services:
  - type: web
    name: blood-management-system
    env: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn blood_management.wsgi:application"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: "*"
      - key: DATABASE_URL
        fromDatabase:
          name: blood_management_db
          property: connectionString
```

### Step 2: Deploy

1. Push code to GitHub
2. Go to https://render.com
3. Click "New" → "Web Service"
4. Connect GitHub repository
5. Configure:
   - Name: blood-management-system
   - Environment: Python 3
   - Build Command: `./build.sh`
   - Start Command: `gunicorn blood_management.wsgi:application`
6. Add environment variables
7. Click "Create Web Service"

---

## 🚂 Deploy to Railway.app

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login and Initialize

```bash
railway login
railway init
```

### Step 3: Add Database

```bash
railway add --plugin postgresql
```

### Step 4: Deploy

```bash
railway up
```

### Step 5: Set Environment Variables

```bash
railway variables set SECRET_KEY=your-secret-key
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=*.railway.app
```

### Step 6: Open App

```bash
railway open
```

---

## 🐍 Deploy to PythonAnywhere

### Step 1: Upload Code

1. Create account at https://www.pythonanywhere.com
2. Go to Files tab
3. Upload project or clone from GitHub

### Step 2: Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 blood_env
pip install -r requirements.txt
```

### Step 3: Configure Web App

1. Go to Web tab → Add a new web app
2. Choose "Manual configuration"
3. Select Python 3.10
4. Set source code: `/home/yourusername/blood-management`
5. Set working directory: `/home/yourusername/blood-management`

### Step 4: Configure WSGI

Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:

```python
import os
import sys

path = '/home/yourusername/blood-management'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'blood_management.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 5: Static Files

In Web tab:
- URL: `/static/`
- Directory: `/home/yourusername/blood-management/staticfiles/`

- URL: `/media/`
- Directory: `/home/yourusername/blood-management/media/`

### Step 6: Reload

Click "Reload" button in Web tab.

---

## 🐳 Deploy with Docker

### Dockerfile

```dockerfile
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Create sample data
RUN python manage.py create_sample_data || true

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "blood_management.wsgi:application"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: blood_management
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn blood_management.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Build and Run

```bash
docker-compose up --build
```

---

## 📧 Configure Email (Gmail)

### 1. Enable 2-Factor Authentication

Go to Google Account → Security → 2-Step Verification

### 2. Generate App Password

Security → App passwords → Generate

### 3. Update settings.py

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-char-app-password'
DEFAULT_FROM_EMAIL = 'Blood Management System <your-email@gmail.com>'
```

---

## 🔒 Security Checklist

Before going live:

- [ ] Change SECRET_KEY to strong random value
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set secure cookies (CSRF, Session)
- [ ] Configure CORS properly
- [ ] Use strong database password
- [ ] Limit database access
- [ ] Enable firewall
- [ ] Regular backups
- [ ] Monitor error logs
- [ ] Set up Sentry for error tracking

---

## 📊 Post-Deployment Tasks

### 1. Create Superuser

```bash
python manage.py createsuperuser
```

### 2. Create Sample Data (Optional)

```bash
python manage.py create_sample_data
```

### 3. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 4. Test Email

Test email functionality in production.

### 5. Monitor

- Check logs regularly
- Monitor database size
- Track error rates
- Monitor response times

---

## 🎯 Custom Domain

### Render.com

1. Go to Settings
2. Click "Add Custom Domain"
3. Enter domain name
4. Add DNS records:
   ```
   CNAME: www → yourapp.onrender.com
   A: @ → <IP from Render>
   ```

### Railway.app

1. Go to Settings
2. Add custom domain
3. Update DNS:
   ```
   CNAME: @ → yourapp.up.railway.app
   ```

---

## 📱 Progressive Web App (Optional)

Add PWA features:

### manifest.json

```json
{
  "name": "Blood Management System",
  "short_name": "Blood Bank",
  "description": "Blood donor and request management system",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#dc3545",
  "icons": [
    {
      "src": "/static/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

---

## 🔄 Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Render
      uses: johnbeynon/render-deploy-action@v0.0.8
      with:
        service-id: ${{ secrets.RENDER_SERVICE_ID }}
        api-key: ${{ secrets.RENDER_API_KEY }}
```

---

## 🆘 Troubleshooting

### Static Files Not Loading

```bash
python manage.py collectstatic --clear --noinput
```

Check STATIC_ROOT and STATIC_URL settings.

### Database Connection Error

Verify DATABASE_URL or database credentials in environment variables.

### 500 Internal Server Error

Check logs:
```bash
# Render
render logs

# Railway
railway logs

# PythonAnywhere
Check error logs in Files tab
```

### Email Not Sending

- Verify SMTP credentials
- Check app password (Gmail)
- Ensure EMAIL_USE_TLS = True
- Check firewall/port 587

---

## 📞 Support

For deployment issues:
- Check platform documentation
- Review error logs
- Search Stack Overflow
- Contact platform support

---

## ✅ Deployment Verification

After deployment:

- [ ] Homepage loads correctly
- [ ] Can register new user
- [ ] Can login
- [ ] Can create donor profile
- [ ] Can upload photos
- [ ] Can create blood request
- [ ] Admin dashboard works
- [ ] Search functionality works
- [ ] Email notifications work
- [ ] Mobile responsive
- [ ] All links work
- [ ] No console errors
- [ ] HTTPS enabled
- [ ] Custom domain (if configured)

---

## 🎉 Success!

Your Blood Management System is now live and helping save lives! 🩸❤️

**Live URL**: https://your-app.onrender.com (or your custom domain)

Share your deployment link in your assignment submission!

---

**Good luck with your deployment!** 🚀
