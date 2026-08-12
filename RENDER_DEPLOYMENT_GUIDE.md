# 🚀 TezSavdo - PRODUCTION READY DEPLOYMENT GUIDE

## ✅ TOLIQ PRODUCTION KONFIGURATSIYA

### 📦 Qo'shilgan Xizmatlar

#### 1. **Web Service** (Gunicorn)
```yaml
startCommand: gunicorn config.wsgi:application
  --workers 3
  --worker-class sync
  --max-requests 1000
  --timeout 120
  --graceful-timeout 30
```
- ✅ 3 Gunicorn workers
- ✅ Request limiting
- ✅ Graceful shutdown
- ✅ Health checks

#### 2. **PostgreSQL Database** 🗄️
```yaml
- type: postgres
  name: tezsavdo-db
  version: "15"
  plan: starter
  region: frankfurt
```
- ✅ Production-grade database
- ✅ 7-day automatic backups
- ✅ Connection pooling
- ✅ Auto connection URLs

#### 3. **Redis Cache** ⚡
```yaml
- type: redis
  name: tezsavdo-cache
  version: "7"
  plan: starter
```
- ✅ Session caching
- ✅ Query result caching
- ✅ Celery broker
- ✅ LRU eviction policy

#### 4. **Celery Worker** 🔄
```yaml
- type: worker
  startCommand: celery -A config worker
    --loglevel=info
    --concurrency=2
    --max-tasks-per-child=1000
```
- ✅ Background async tasks
- ✅ Email sending
- ✅ Data processing
- ✅ Report generation

#### 5. **Cron Jobs** ⏰
```yaml
crons:
  - cleanup-sessions: Daily at 2 AM UTC
  - send-admin-reports: Daily at 8 AM UTC
  - database-backup: Daily at 4 AM UTC
  - cleanup-old-media: Weekly on Sunday
```

---

## 🛠️ RENDER-DA SOZLASH UCHUN KERAKLI ENV VARIABLES

### Render Dashboard-da o'rnating:

```
# ========== DJANGO ==========
DEBUG=False
SECRET_KEY=<generate-64-character-random-string>
DJANGO_SETTINGS_MODULE=config.settings
ALLOWED_HOSTS=tezsavdo-777.onrender.com,localhost,127.0.0.1

# ========== DATABASE (AUTO) ==========
# DATABASE_URL otomatik Render-dan o'qilinadi
# Shuning uchun ko'rsatish shart emas

# ========== REDIS (AUTO) ==========
# REDIS_URL otomatik Render-dan o'qilinadi

# ========== CELERY ==========
# CELERY_BROKER_URL va CELERY_RESULT_BACKEND
# settings.py-da REDIS_URL-dan o'qilinadi

# ========== EMAIL ==========
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@tezsavdo.uz

# ========== SECURITY ==========
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https

# ========== MONITORING ==========
SENTRY_DSN=<if-using-sentry>
ENVIRONMENT=production

# ========== API ==========
CORS_ALLOWED_ORIGINS=https://tezsavdo-777.onrender.com,https://www.tezsavdo.uz

# ========== PYTHON ==========
PYTHON_UNBUFFERED=1
PYTHONUNBUFFERED=1
WEB_CONCURRENCY=3
```

---

## 📋 RENDER-DA DEPLOY QILISH STEPS

### 1️⃣ **Render-da yangi Web Service yarating**
   - Service name: `tezsavdo`
   - Repository: `https://github.com/zahon1300-boop/tezsavdo.git`
   - Branch: `main`
   - Environment: `Python`
   - Build Command: render.yaml-da belgilangan (auto)
   - Start Command: render.yaml-da belgilangan (auto)

### 2️⃣ **Render UI-da services ulang** (YAML-dan oqilib yoqadi):
   - `tezsavdo` Web Service
   - `tezsavdo-db` PostgreSQL
   - `tezsavdo-cache` Redis
   - `tezsavdo-worker` Celery Worker (opsional, keyinroq activate qilish mumkin)

### 3️⃣ **Environment variables-ni o'rnating** (Render Dashboard):
   - Database va Redis URLs otomatik o'qilinadi
   - SECRET_KEY, EMAIL, CORS qo'shining
   - .env.example-dan misol oling

### 4️⃣ **Deploy ni boshlang**:
   - Auto-deploy enabled
   - ~5-10 minut build va deploy vaqti

---

## 📊 Qo'shilgan Yangi Features

### ✨ Logging System
```python
# /logs/django.log-ga rotated logs
# Production error tracking
# 15MB rotating files, 10 backup
```

### 🔐 Security
```python
# HSTS, CSP, XSS protection
# Secure cookies (HTTPS only)
# CSRF protection
# SQL injection prevention (Django ORM)
```

### 📧 Email System
```python
# Gmail SMTP integration ready
# Email-based notifications
# Task-based email sending (async)
```

### 📈 API Rate Limiting
```python
# Anonymous: 100 requests/hour
# Authenticated: 1000 requests/hour
```

### 🔔 Monitoring Ready
```python
# Sentry.io integration ready
# Error tracking va alerting
# Performance monitoring
```

### 💼 Async Tasks (Celery)
```python
# Background processing
# Email sending
# Report generation
# Scheduled jobs (Cron)
# Data cleanup
```

---

## 🎯 Deployment Checklist

- ✅ `render.yaml` - Toliq konfiguratsiya
- ✅ `requirements.txt` - Barcha dependencies
- ✅ `config/celery.py` - Celery setup
- ✅ `shop/tasks.py` - Async tasks
- ✅ `config/settings.py` - Production settings
- ✅ `.env.example` - Environment template
- ✅ `logs/` - Directory created
- ✅ GitHub - Barcha push qilindi
- ✅ Django check - ✓ Passed
- ✅ Migrations - Ready
- ✅ Static files - collectstatic qilingan

---

## 📱 POST-DEPLOYMENT

### 1. Login to Admin
```
https://tezsavdo-777.onrender.com/admin/
```

### 2. Create Superuser
```bash
python manage.py createsuperuser
```

### 3. Seed Sample Data (opsional)
```bash
python manage.py seed_products --count 100
```

### 4. Monitor Celery (optional)
```bash
# Flower UI uchun (task monitoring dashboard)
# redis-cli ping (Redis connection test)
```

---

## 🚨 TROUBLESHOOTING

### 400 Bad Request
- ✅ **Fixed**: ALLOWED_HOSTS-da `*.onrender.com` qo'shildi

### Static files not loading
- ✅ **Fixed**: WhiteNoise middleware enabled + collectstatic in build

### Database connection error
- ✅ **Fix**: PostgreSQL service ulanganligini tekshiring + DATABASE_URL-ni o'rnating

### Redis connection error
- ✅ **Fix**: Redis service ulanganligini tekshiring + REDIS_URL-ni o'rnating

### Email not sending
- ✅ **Fix**: Gmail app password-i (regular password emas) ishlatiding

---

## 📊 Performance Tips

1. **Workers**: 3 workers optimal 512MB memory uchun
2. **Database**: Connection pooling enabled (conn_max_age=600)
3. **Cache**: Redis enabled barcha queries-ni cache qilish uchun
4. **Static**: WhiteNoise bilan optimized delivery
5. **Logging**: Production-grade rotating logs

---

## 🔗 Foydali Linklar

- 📚 [Render Docs](https://render.com/docs)
- 🐘 [PostgreSQL Docs](https://www.postgresql.org/docs)
- 📮 [Django Email Docs](https://docs.djangoproject.com/en/5.0/topics/email)
- 🔄 [Celery Docs](https://docs.celeryio.org)
- ⚡ [Redis Docs](https://redis.io/documentation)

---

## ✅ STATUS: PRODUCTION READY! 🎉

**Sayt Render-da deployment ga 100% tayyor!**

Hamma dependency'lar, konfiguratsiyalar, va security sozlamalari qilingan.

**NEXT STEP:** Render Dashboard-da environment variables-ni o'rnating va DEPLOY QILING! 🚀

---

**Generated:** 2026-08-12
**Version:** 1.0.0 (Production Ready)
**Last Updated:** Latest commit (7145758)
