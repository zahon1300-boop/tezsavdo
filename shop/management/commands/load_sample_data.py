from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Kategoriya, Brend, Mahsulot, MahsulotRasm, Aktsiya, Kupon, Banner, ViloyatRaioni, SaytSozlamalar, SaytMalumotlari, DemoKarta
import random


class Command(BaseCommand):
    help = '100 ta kategoriya va har biriga 50 tadan mahsulot yuklash'

    def handle(self, *args, **kwargs):
        self.stdout.write('Kategoriyalar va mahsulotlar yuklanmoqda...')

        Mahsulot.objects.all().delete()
        Kategoriya.objects.all().delete()
        Brend.objects.all().delete()
        ViloyatRaioni.objects.all().delete()
        Aktsiya.objects.all().delete()
        Kupon.objects.all().delete()
        Banner.objects.all().delete()

        kategoriya_nomlari = [
            'Smartfonlar', 'Noutbuklar', 'Planshetlar', 'Televizorlar', 'Audio uskunalar',
            'Kamera va foto', 'Oshxona texnikasi', 'Kir yuvish mashinasi', 'Sovutgich', 'Changyutgich',
            'Mikroto\'lqinli pech', 'Elektr choynak', 'Elektr maydalagich', 'Qahva mashinasi', 'Blender',
            'Fen', 'Tersker', 'Dazmollar', 'Sichqoncha', 'Klaviatura',
            'Monitor', 'Printer', 'Uy router', 'Quloqchin', 'Kutubxona',
            'Sport kiyim', 'Erkaklar kiyim', 'Ayollar kiyim', 'Bolalar kiyim', 'Oyoq kiyim',
            'Sumka', 'Soat', 'Zargar', 'Ko\'zoynak', 'Parfyumeriya',
            'Makiyaj', 'Parvarish vositalari', 'Shampun', 'Tish pastasi', 'Duradgor',
            'Uy tekstil', 'Oshxona idishi', 'Chiroq', 'Devor bezagi', 'Gul',
            'O\'yinchoq', 'Kitob', 'Darslik', 'Kantstovar', 'Bolalar o\'ynash',
            'Uy hayvonlari', 'Oziq-ovqat', 'Ichimlik', 'Shirinlik', 'Meva',
            'Sabzavot', 'Non va mahsulot', 'Go\'sht va baliq', 'Sut va tvorog', 'Yogurt',
            'Avtomobil ehtiyot qismi', 'Moylash', 'Shina', 'Akumulyator', 'Avtomobil audio',
            'Datchik', 'Xavfsizlik kamera', 'Signalizatsiya', 'GPS navigator', 'Avtomobil aksessuar',
            'Velosiped', 'Scooter', 'Yugurish', 'Futbol', 'Basketbol',
            'Tennis', 'Suzish', 'Fitness', 'Yoga', 'Boks',
            'Qishki sport', 'Suzish kiyim', 'Sayohat', 'Suitcase', 'Rucksak',
            'Guitar', 'Pianino', 'Davul', 'Chalg\'u', 'Audiokniga',
            'Telefon aksessuar', 'Zaryad qurilma', 'Powerbank', 'USB kabel', 'Bluetooth adapter',
            'Kiyim aksessuar', 'Kamiz', 'Sharf', 'Bant', 'Bog\'cha',
            'Komp\'yuter', 'Server', 'Kamer\'a', 'Dasturlash', 'Bulutli xizmat'
        ]

        kategoriyalar = []
        for nom in kategoriya_nomlari:
            kat, _ = Kategoriya.objects.get_or_create(nom=nom, defaults={'slug': slugify(nom)})
            kategoriyalar.append(kat)

        brendlar = [
            'Samsung', 'Apple', 'Xiaomi', 'LG', 'Sony', 'Nike', 'Adidas', 'Zara', 'H&M',
            'Bosch', 'Philips', 'Panasonic', 'Canon', 'Nikon', 'Puma', 'Reebok', 'New Balance',
            'Under Armour', 'The North Face', 'Columbia', 'Dell', 'HP', 'Lenovo', 'Asus',
            'Acer', 'Microsoft', 'Google', 'Huawei', 'Oppo', 'Vivo', 'OnePlus', 'Realme',
            ' Tecno', 'Infinix', 'Honor', 'Meizu', 'Nothing', 'Motorola', 'Fairphone', 'Shift'
        ]
        for nom in brendlar:
            Brend.objects.get_or_create(nom=nom, defaults={'slug': slugify(nom)})

        viloyatlar = [
            ('Toshkent', 'Chilonzor', 15000), ('Toshkent', 'Yunusabad', 15000),
            ('Toshkent', 'Mirzo Ulug\'bek', 15000), ('Toshkent', 'Uchtepa', 12000),
            ('Toshkent', 'Yakasaray', 10000), ('Toshkent', 'Shaykhontohur', 10000),
            ('Toshkent', 'Olmazor', 12000), ('Toshkent', 'Bektemir', 15000),
            ('Toshkent', 'Sirg\'ali', 12000), ('Toshkent', 'Yangiyo\'l', 15000),
            ('Samarqand', 'Samarqand shahar', 20000), ('Samarqand', 'Kattaqo\'rg\'on', 25000),
            ('Buxoro', 'Buxoro shahar', 20000), ('Buxoro', 'G\'ijduvon', 25000),
            ('Xorazm', 'Urganch', 25000), ('Xorazm', 'Xiva', 30000),
            ('Andijon', 'Andijon shahar', 20000), ('Andijon', 'Asaka', 25000),
            ('Farg\'ona', 'Farg\'ona shahar', 20000), ('Farg\'ona', 'Qo\'qon', 22000),
            ('Namangan', 'Namangan shahar', 20000), ('Namangan', 'Chust', 25000),
            ('Qashqadaryo', 'Qarshi', 25000), ('Qashqadaryo', 'Shahrisabz', 28000),
            ('Surxondaryo', 'Termiz', 30000), ('Surxondaryo', 'Denov', 28000),
            ('Jizzax', 'Jizzax shahar', 20000), ('Jizzax', 'G\'allaorol', 25000),
            ('Navoiy', 'Navoiy shahar', 20000), ('Navoiy', 'Zarafshon', 22000),
            ('Sirdaryo', 'Guliston', 20000), ('Sirdaryo', 'Shirin', 25000),
            ('Qoraqalpog\'iston', 'Nukus', 25000), ('Qoraqalpog\'iston', 'Beruniy', 30000),
        ]
        for viloyat, raion, narx in viloyatlar:
            ViloyatRaioni.objects.get_or_create(
                viloyat=viloyat,
                raion=raion,
                defaults={'yetkazish_narxi': narx, 'kunlar': 1}
            )

        aktsiyalar = [
            {'nom': 'Yozgi super sotuv', 'tavsif': 'Barcha mahsulotlarda 50% gacha chegirma', 'boshlanish': '2024-06-01', 'tugash': '2024-08-31', 'chegirma_foiz': 50},
            {'nom': 'Yangi yil aksiyasi', 'tavsif': 'Yangi yil oldidan katta sotuv', 'boshlanish': '2024-12-20', 'tugash': '2025-01-10', 'chegirma_foiz': 30},
            {'nom': 'Sport anjomlari chegirmasi', 'tavsif': 'Sport mahsulotlarida maxsus narxlar', 'boshlanish': '2024-07-01', 'tugash': '2024-09-01', 'chegirma_foiz': 40},
        ]
        for data in aktsiyalar:
            Aktsiya.objects.get_or_create(nom=data['nom'], defaults=data)

        kuponlar = [
            {'kod': 'TEZSAVDO10', 'nom': '10% chegirma', 'turi': 'foiz', 'qiymat': 10, 'boshlanish': '2024-01-01', 'tugash': '2025-12-31'},
            {'kod': 'TEZSAVDO20', 'nom': '20% chegirma', 'turi': 'foiz', 'qiymat': 20, 'boshlanish': '2024-01-01', 'tugash': '2025-12-31'},
            {'kod': 'BONUS50000', 'nom': '50000 so\'m chegirma', 'turi': 'summa', 'qiymat': 50000, 'boshlanish': '2024-01-01', 'tugash': '2025-12-31'},
        ]
        for data in kuponlar:
            Kupon.objects.get_or_create(kod=data['kod'], defaults=data)

        bannerlar = [
            {'nom': 'Yozgi aksiya', 'matn': '50% gacha chegirma', 'pozitsiya': 'bosh', 'tartib': 1},
            {'nom': 'Yangi mahsulotlar', 'matn': 'Yangi kolleksiya', 'pozitsiya': 'bosh', 'tartib': 2},
            {'nom': 'Bepul yetkazish', 'matn': '200000 so\'mdan boshlab bepul', 'pozitsiya': 'bosh', 'tartib': 3},
        ]
        for data in bannerlar:
            Banner.objects.get_or_create(nom=data['nom'], defaults=data)

        SaytSozlamalar.objects.get_or_create(kalit='sayt_nomi', defaults={'qiymat': 'TezSavdo'})
        SaytSozlamalar.objects.get_or_create(kalit='telefon', defaults={'qiymat': '+998 90 123 45 67'})
        SaytSozlamalar.objects.get_or_create(kalit='email', defaults={'qiymat': 'info@tezsavdo.uz'})
        SaytSozlamalar.objects.get_or_create(kalit='manzil', defaults={'qiymat': 'Buxoro viloyati, Vobkent tumani, Kolxatib MFY, 41-uy'})

        sayt_malumotlari = [
            {'nom': 'telegram', 'qiymat': 'https://t.me/jahon_dev'},
            {'nom': 'youtube', 'qiymat': 'https://www.youtube.com/@joraqulov_777'},
            {'nom': 'instagram', 'qiymat': 'https://www.instagram.com/jahon_dev'},
            {'nom': 'ish_vaqti_dushanba_juma', 'qiymat': '09:00 - 20:00'},
            {'nom': 'ish_vaqti_shanba', 'qiymat': '10:00 - 18:00'},
            {'nom': 'ish_vaqti_yakshanba', 'qiymat': 'Dam olish kuni'},
        ]
        for data in sayt_malumotlari:
            SaytMalumotlari.objects.get_or_create(nom=data['nom'], defaults=data)

        demo_kartalar = [
            {'nom': 'Demo UzCard 1', 'tur': 'uzcard', 'karta_raqami': '8600123456789012', 'amal_qilish_muddati': '12/28', 'balans': 5000000},
            {'nom': 'Demo Humo 1', 'tur': 'humo', 'karta_raqami': '8600987654321098', 'amal_qilish_muddati': '12/28', 'balans': 3000000},
            {'nom': 'Demo Visa 1', 'tur': 'visa', 'karta_raqami': '4111111111111111', 'amal_qilish_muddati': '12/28', 'balans': 10000000},
            {'nom': 'Demo MasterCard 1', 'tur': 'mastercard', 'karta_raqami': '5500000000000004', 'amal_qilish_muddati': '12/28', 'balans': 8000000},
        ]
        for data in demo_kartalar:
            DemoKarta.objects.get_or_create(karta_raqami=data['karta_raqami'], defaults=data)

        self.stdout.write('5000 ta mahsulot yaratilmoqda...')
        brendlar_list = list(Brend.objects.all())
        for kategoriya in kategoriyalar:
            for i in range(1, 51):
                nom = f"{kategoriya.nom} - Mahsulot {i}"
                narx = random.randint(10000, 5000000)
                eski_narx = random.randint(narx + 10000, narx + 500000) if random.random() > 0.5 else None
                mahsulot = Mahsulot.objects.create(
                    nom=nom,
                    kategoriya=kategoriya,
                    brend=random.choice(brendlar_list) if brendlar_list else None,
                    tavsif=f"Bu juda ham sifatli {kategoriya.nom.lower()} mahsuloti. Zamonaviy dizayn va yuqori sifat.",
                    narx=narx,
                    eski_narx=eski_narx,
                    soni=random.randint(0, 100),
                    is_active=True,
                    yangi=random.random() > 0.7,
                    oxirgi=random.random() > 0.8,
                    tavsiya_etilgan=random.random() > 0.9,
                )

        self.stdout.write(self.style.SUCCESS('100 ta kategoriya va 5000 ta mahsulot yuklandi!'))
