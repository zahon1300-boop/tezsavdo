# TezSavdo Deployment Guide

## Production Settings

1. Install production dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgres://user:pass@host:5432/dbname  # Optional for PostgreSQL
```

3. Collect static files:
```bash
python manage.py collectstatic --noinput
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Seed products (optional):
```bash
python manage.py seed_products --count 100
```

7. Run with gunicorn:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Using Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Environment Variables

- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to False in production
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DATABASE_URL` - PostgreSQL connection string (optional)
- `MEDIA_ROOT` - Path to media files
- `STATIC_ROOT` - Path to static files

## Notes

- Default language: Uzbek (uz)
- Supported languages: Uzbek (uz), Russian (ru), English (en)
- Admin panel: /admin/
- Site URL: / (redirects to /uz/ by default)
