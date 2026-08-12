# TEZSAVDO — Professional E-Commerce Platform

O'zbekistondagi professional onlayn do'kon platformasi.

## Texnologiyalar

- Python 3.12+
- Django 5+
- SQLite (development)
- HTML5 / CSS3 / JavaScript ES6+
- Bootstrap 5
- Django Templates
- Pillow

## O'rnatish

```bash
# Virtual environment yaratish
python -m venv venv
venv\Scripts\activate  # Windows
# yoki
source venv/bin/activate  # Linux/Mac

# Kutubxonalarni o'rnatish
pip install -r requirements.txt

# .env fayl yaratish
cp .env.example .env

# Migratsiyalar
python manage.py makemigrations
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Seed data (test mahsulotlari)
python manage.py seed_data

# Serverni ishga tushirish
python manage.py runserver
```

## Admin Panel

```
http://127.0.0.1:8000/admin/
```

## Foydalanuvchi Panel

```
http://127.0.0.1:8000/
```

## Test

```bash
python manage.py check
python manage.py test
```

## Loyiha tuzilishi

```
tezsavdo/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   ├── urls.py
│   └── migrations/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── mahsulotlar.html
│   ├── mahsulot_detali.html
│   ├── savatcha.html
│   ├── checkout.html
│   └── ...
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
├── media/
├── requirements.txt
├── .gitignore
└── README.md
```

## Asosiy funksiyalar

- [x] Mahsulotlar katalogi
- [x] Qidiruv va filter
- [x] Mahsulot detali
- [x] Variant tanlash (rang, xotira, storage)
- [x] Savatcha (cart)
- [x] Wishlist
- [x] Checkout
- [x] Buyurtmalar
- [x] Foydalanuvchi profili
- [x] Admin panel
- [x] Dark/Light mode
- [x] Responsive dizayn

## License

Private - All rights reserved
