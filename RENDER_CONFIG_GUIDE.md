# Render Deployment Configuration Guide

## 📋 render.yaml Konfiguratsiyasi

Quyidagi asosiy konfiguratsiyalar qo'shildi:

### 1. **Web Service Settings**
```yaml
region: frankfurt          # Server manzili (eng yaqin serverdan tanlang)
plan: standard            # Performance plani
autoDeploy: true          # Avtomatik deploy
healthCheckPath: /admin/  # Health check URL
healthCheckTimeout: 30    # Timeout (sekund)
```

### 2. **Environment Variables**
```yaml
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings
PYTHON_UNBUFFERED=1    # Real-time console output
```

### 3. **Disk Storage (Media fayllar)**
```yaml
disk:
  name: media-storage
  mountPath: /opt/render/media
  sizeGB: 10             # Media fayllar uchun 10GB
```

### 4. **Pre-deploy Script**
```yaml
preDeployCommand: python manage.py migrate --noinput
```

### 5. **Log Retention**
```yaml
logRetentionDays: 30     # Loglarni 30 kun saqlash
```

---

## 📊 PostgreSQL Database (Tavsiya Etiladi)

SQLite o'rniga PostgreSQL-dan foydalaning production-da:

### Render-da PostgreSQL yaratish:
1. Render dashboard-ga kiring
2. "PostgreSQL" tanlang
3. Tarifni tanlang (Starter - FREE)
4. Region: Frankfurt (app bilan bir xil)
5. Database yarating

### `settings.py`-ga Qo'shish:
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
```

### requirements.txt-ga Qo'shish:
```
dj-database-url==2.1.0
psycopg2-binary==2.9.9   # Allaqachon bor
```

---

## 🔄 Celery Background Jobs (Opsional)

Agar asynchronous tasks kerak bo'lsa:

### 1. requirements.txt-ga Qo'shish:
```
celery==5.3.4
redis==5.0.1
```

### 2. render.yaml-ga Worker Qo'shish:
```yaml
workers:
  - type: worker
    name: tezsavdo-celery
    env: python
    startCommand: celery -A config worker -l info
```

### 3. Redis Service Yaratish (Render-da)
- Redis cache service yarating
- Connection URL ni environment variable qo'ying

---

## ⏰ Scheduled Jobs (Cron)

Masalan: har kuni session cleanup

### render.yaml-ga:
```yaml
crons:
  - id: cleanup-sessions
    command: python manage.py clearsessions
    schedule: "0 2 * * *"  # Har kuni 02:00 UTC
  
  - id: cleanup-media
    command: python manage.py cleanup_old_files
    schedule: "0 3 * * 0"  # Har yakshanba 03:00 UTC
```

---

## 🔐 Environment Variables (RENDER-DA O'RNATING)

Qo'lda Render dashboard-da kiriting:

```
# Security
DEBUG=False
SECRET_KEY=your-super-secure-random-64-char-key-here

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Domain
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com

# Email (opsional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 (opsional, static/media uchun)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1
```

---

## 📦 Static & Media Files - 3 Variant

### Variant 1: Render Disk (Eng Oddiy)
```yaml
disk:
  name: media-storage
  mountPath: /opt/render/media
  sizeGB: 10
```

### Variant 2: AWS S3 (Eng Yaxshi - Scalable)
#### requirements.txt-ga:
```
boto3==1.34.0
django-storages==1.14.2
```

#### settings.py-ga:
```python
if not DEBUG:
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
            'OPTIONS': {
                'bucket_name': os.environ.get('AWS_STORAGE_BUCKET_NAME'),
            }
        },
    }
```

### Variant 3: Cloudinary (Eng Oson)
```python
MEDIA_URL = 'https://res.cloudinary.com/account-name/image/upload/'
```

---

## 🚀 Deploy Qilish Bosqichlari

1. **Repository tayyorlash:**
   ```bash
   git add render.yaml
   git commit -m "Enhanced Render configuration"
   git push origin main
   ```

2. **Render-da Web Service yaratish:**
   - Repository: `https://github.com/zahon1300-boop/tezsavdo.git`
   - Branch: `main`
   - Build command: `render.yaml`-dan avtomatik o'qiladi
   - Environment variables: Render dashboard-da o'rnating

3. **PostgreSQL (opsional) yaratish:**
   - Render dashboard → PostgreSQL
   - DATABASE_URL ni environment variable sifatida qo'ying

4. **Deploy tugmasini bosing!**

---

## ✅ Deployment Checklist

- ✅ `render.yaml` to'liq konfiguratsiyalangan
- ✅ `requirements.txt` barcha paketlar bor
- ✅ `settings.py` production-ready
- ✅ Environment variables ready (Render-da o'rnating)
- ✅ Git pushed
- ✅ Health check path ko'rsatilgan
- ✅ Media storage konfiguratsiyalangan

---

## 🔧 Render Deployment Advanced Tips

### 1. **Region Tanlash**
- Frankfurt: Europe
- Ohio: North America
- Singapore: Asia
- Mumbai: India

### 2. **Worker Count**
- 4 workers - Standard
- 2 workers - Budget
- 8+ workers - High traffic

### 3. **Database Connection Pooling**
```python
DATABASES['default']['CONN_MAX_AGE'] = 600
DATABASES['default']['CONN_HEALTH_CHECKS'] = True
```

### 4. **Caching**
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/1'),
    }
}
```

---

## 📞 Render Docs
- https://render.com/docs
- https://render.com/docs/deploy-django

---

Generated: 2026-08-12
