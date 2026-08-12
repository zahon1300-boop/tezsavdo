import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from shop.models import *


class Command(BaseCommand):
    help = 'Seed database with realistic e-commerce products'
    
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=500, help='Number of products to create')
        parser.add_argument('--clear-demo', action='store_true', help='Clear existing demo data')
        parser.add_argument('--force', action='store_true', help='Force recreate even if data exists')

    def handle(self, *args, **options):
        count = options['count']
        clear_demo = options['clear_demo']
        force = options['force']
        
        if clear_demo:
            self.clear_data()
            self.stdout.write(self.style.SUCCESS('Demo data cleared'))
            return
        
        if force:
            self.clear_data()
            self.stdout.write('Existing data cleared for force recreate...')
        
        if not force and Mahsulot.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists. Use --force to recreate or --clear-demo to clear'))
            return
        
        self.stdout.write('Starting seed process...')
        
        with transaction.atomic():
            option_types = self.create_option_types()
            categories, brands = self.create_categories_and_brands()
            products_data = self.get_products_data()
            
            total_products = 0
            total_variants = 0
            total_images = 0
            
            for product_info in products_data[:count]:
                product = self.create_product(product_info, categories, brands)
                if product:
                    variants_count = self.create_variants(product, option_types, product_info)
                    total_variants += variants_count
                    total_products += 1
            
            self.stdout.write(self.style.SUCCESS(f'SEED REPORT'))
            self.stdout.write(f'Products: {total_products}')
            self.stdout.write(f'Variants: {total_variants}')
            self.stdout.write(f'Brands: {Brend.objects.count()}')
            self.stdout.write(f'Categories: {Kategoriya.objects.count()}')
            self.stdout.write(f'Option Types: {OptionType.objects.count()}')
            self.stdout.write(f'Option Values: {OptionValue.objects.count()}')

    def clear_data(self):
        MahsulotVariant.objects.all().delete()
        VariantOption.objects.all().delete()
        VariantRasm.objects.all().delete()
        MahsulotRasm.objects.all().delete()
        Mahsulot.objects.all().delete()
        OptionValue.objects.all().delete()
        OptionType.objects.all().delete()
        Brend.objects.all().delete()
        Kategoriya.objects.filter(parent__isnull=False).delete()
        Kategoriya.objects.filter(parent__isnull=True).delete()

    def create_option_types(self):
        option_types_data = [
            ('Rang', 'color', 'color', 1),
            ('Xotira', 'storage', 'text', 2),
            ('RAM', 'ram', 'text', 3),
            ('Protsessor', 'processor', 'text', 4),
            ('GPU', 'gpu', 'text', 5),
            ('Ekran o\'lchami', 'screen_size', 'text', 6),
            ('Rang', 'color', 'color', 1),
        ]
        
        option_types = {}
        for nom, kalit, turi, tartib in option_types_data:
            ot, _ = OptionType.objects.get_or_create(
                kalit=kalit,
                defaults={'nom': nom, 'turi': turi, 'tartib': tartib}
            )
            option_types[kalit] = ot
        return option_types

    def create_categories_and_brands(self):
        categories_data = {
            'Smartfonlar': {
                'sub': ['Apple iPhone', 'Samsung Galaxy', 'Xiaomi', 'Redmi', 'POCO', 'Honor', 'OPPO', 'vivo', 'Realme', 'Nokia'],
                'icon': 'fa-mobile-alt'
            },
            'Noutbuklar': {
                'sub': ['Apple MacBook', 'ASUS', 'Lenovo', 'HP', 'Dell', 'Acer', 'MSI', 'Huawei'],
                'icon': 'fa-laptop'
            },
            'Planshetlar': {
                'sub': ['Apple iPad', 'Samsung Galaxy Tab', 'Xiaomi Pad', 'Lenovo Tab'],
                'icon': 'fa-tablet-alt'
            },
            'Aksessuarlar': {
                'sub': ['Quloqchinlar', 'Soatlar', 'Zaryadlovchilar', 'Kabelalar', 'Kumush', 'Sumkalar'],
                'icon': 'fa-headphones'
            },
            'Televizorlar': {
                'sub': ['Samsung TV', 'LG TV', 'Sony TV', 'Hisense', 'Xiaomi TV'],
                'icon': 'fa-tv'
            },
        }
        
        categories = {}
        brands = {}
        
        for cat_nom, data in categories_data.items():
            cat, _ = Kategoriya.objects.get_or_create(
                nom=cat_nom,
                defaults={'is_active': True}
            )
            categories[cat_nom] = cat
            
            for sub_nom in data['sub']:
                Kategoriya.objects.get_or_create(
                    nom=sub_nom,
                    parent=cat,
                    defaults={'is_active': True}
                )
        
        brands_data = [
            'Apple', 'Samsung', 'Xiaomi', 'Redmi', 'POCO', 'Honor', 'OPPO', 'vivo', 'Realme',
            'ASUS', 'Lenovo', 'HP', 'Dell', 'Acer', 'MSI', 'Huawei',
            'Sony', 'LG', 'Hisense', 'TCL', 'Nokia', 'Motorola',
            'JBL', 'Sennheiser'
        ]
        
        for i, brand_nom in enumerate(brands_data):
            slug = f"{slugify(brand_nom)}-{i}"
            brand, _ = Brend.objects.get_or_create(
                nom=brand_nom,
                defaults={'slug': slug, 'is_active': True}
            )
            brands[brand_nom] = brand
        
        return categories, brands

    def get_products_data(self):
        return [
            {'name': 'iPhone 16 Pro Max', 'category': 'Apple iPhone', 'brand': 'Apple', 'base_price': 15000000, 'options': {'color': ['Qora', 'Oq', 'Titanium', 'Yashil'], 'storage': ['256 GB', '512 GB', '1 TB'], 'ram': ['8 GB']}},
            {'name': 'iPhone 16 Pro', 'category': 'Apple iPhone', 'brand': 'Apple', 'base_price': 13500000, 'options': {'color': ['Qora', 'Oq', 'Titanium', 'Yashil'], 'storage': ['128 GB', '256 GB', '512 GB'], 'ram': ['8 GB']}},
            {'name': 'iPhone 16', 'category': 'Apple iPhone', 'brand': 'Apple', 'base_price': 12000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Yashil', 'Pushti'], 'storage': ['128 GB', '256 GB', '512 GB'], 'ram': ['8 GB']}},
            {'name': 'iPhone 15 Pro Max', 'category': 'Apple iPhone', 'brand': 'Apple', 'base_price': 14000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Yashil'], 'storage': ['256 GB', '512 GB', '1 TB'], 'ram': ['8 GB']}},
            {'name': 'iPhone 15 Pro', 'category': 'Apple iPhone', 'brand': 'Apple', 'base_price': 12500000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Yashil'], 'storage': ['128 GB', '256 GB', '512 GB'], 'ram': ['8 GB']}},
            {'name': 'iPhone 15', 'category': 'Apple iPhone', 'brand': 'Apple', 'base_price': 11000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Yashil', 'Pushti'], 'storage': ['128 GB', '256 GB', '512 GB'], 'ram': ['6 GB']}},
            {'name': 'iPhone 14 Pro Max', 'category': 'Apple iPhone', 'brand': 'Apple', 'base_price': 13000000, 'options': {'color': ['Qora', 'Oq', 'Binafsha', 'Yashil'], 'storage': ['128 GB', '256 GB', '512 GB'], 'ram': ['6 GB']}},
            {'name': 'iPhone 14', 'category': 'Apple iPhone', 'brand': 'Apple', 'base_price': 10000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Qizil'], 'storage': ['128 GB', '256 GB', '512 GB'], 'ram': ['6 GB']}},
            {'name': 'Samsung Galaxy S24 Ultra', 'category': 'Samsung Galaxy', 'brand': 'Samsung', 'base_price': 14500000, 'options': {'color': ['Qora', 'Oq', 'Jigar', 'Kulrang'], 'storage': ['256 GB', '512 GB', '1 TB'], 'ram': ['12 GB']}},
            {'name': 'Samsung Galaxy S24+', 'category': 'Samsung Galaxy', 'brand': 'Samsung', 'base_price': 12000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Yashil'], 'storage': ['128 GB', '256 GB', '512 GB'], 'ram': ['12 GB']}},
            {'name': 'Samsung Galaxy S24', 'category': 'Samsung Galaxy', 'brand': 'Samsung', 'base_price': 10000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Yashil'], 'storage': ['128 GB', '256 GB'], 'ram': ['8 GB']}},
            {'name': 'Samsung Galaxy S23 Ultra', 'category': 'Samsung Galaxy', 'brand': 'Samsung', 'base_price': 13000000, 'options': {'color': ['Qora', 'Oq', 'Binafsha', 'Yashil'], 'storage': ['256 GB', '512 GB', '1 TB'], 'ram': ['12 GB']}},
            {'name': 'Samsung Galaxy A55', 'category': 'Samsung Galaxy', 'brand': 'Samsung', 'base_price': 5500000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Yashil'], 'storage': ['128 GB', '256 GB'], 'ram': ['8 GB']}},
            {'name': 'Samsung Galaxy A35', 'category': 'Samsung Galaxy', 'brand': 'Samsung', 'base_price': 4000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Yashil'], 'storage': ['128 GB', '256 GB'], 'ram': ['6 GB', '8 GB']}},
            {'name': 'Xiaomi 14 Ultra', 'category': 'Xiaomi', 'brand': 'Xiaomi', 'base_price': 12000000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['256 GB', '512 GB', '1 TB'], 'ram': ['12 GB', '16 GB']}},
            {'name': 'Xiaomi 14', 'category': 'Xiaomi', 'brand': 'Xiaomi', 'base_price': 9000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Yashil'], 'storage': ['128 GB', '256 GB', '512 GB'], 'ram': ['8 GB', '12 GB']}},
            {'name': 'Xiaomi 13T Pro', 'category': 'Xiaomi', 'brand': 'Xiaomi', 'base_price': 7500000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k'], 'storage': ['256 GB', '512 GB'], 'ram': ['12 GB']}},
            {'name': 'Redmi Note 13 Pro+', 'category': 'Redmi', 'brand': 'Redmi', 'base_price': 4500000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Pushti'], 'storage': ['128 GB', '256 GB', '512 GB'], 'ram': ['8 GB', '12 GB']}},
            {'name': 'Redmi Note 13 Pro', 'category': 'Redmi', 'brand': 'Redmi', 'base_price': 3500000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k'], 'storage': ['128 GB', '256 GB'], 'ram': ['8 GB', '12 GB']}},
            {'name': 'POCO X6 Pro', 'category': 'POCO', 'brand': 'POCO', 'base_price': 4000000, 'options': {'color': ['Qora', 'Oq', 'Sariq'], 'storage': ['128 GB', '256 GB', '512 GB'], 'ram': ['8 GB', '12 GB']}},
            {'name': 'POCO F6 Pro', 'category': 'POCO', 'brand': 'POCO', 'base_price': 5500000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['256 GB', '512 GB'], 'ram': ['12 GB']}},
            {'name': 'Honor Magic6 Pro', 'category': 'Honor', 'brand': 'Honor', 'base_price': 9000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k'], 'storage': ['256 GB', '512 GB'], 'ram': ['12 GB', '16 GB']}},
            {'name': 'MacBook Pro 16 M3 Max', 'category': 'Apple MacBook', 'brand': 'Apple', 'base_price': 45000000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['512 GB', '1 TB', '2 TB'], 'ram': ['36 GB', '48 GB', '128 GB']}},
            {'name': 'MacBook Pro 14 M3 Pro', 'category': 'Apple MacBook', 'brand': 'Apple', 'base_price': 32000000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['512 GB', '1 TB'], 'ram': ['18 GB', '36 GB']}},
            {'name': 'MacBook Air 15 M3', 'category': 'Apple MacBook', 'brand': 'Apple', 'base_price': 22000000, 'options': {'color': ['Qora', 'Oq', 'Yashil', 'Ko\'k', 'Pushti'], 'storage': ['256 GB', '512 GB', '1 TB'], 'ram': ['8 GB', '16 GB', '24 GB']}},
            {'name': 'MacBook Air 13 M3', 'category': 'Apple MacBook', 'brand': 'Apple', 'base_price': 18000000, 'options': {'color': ['Qora', 'Oq', 'Yashil', 'Ko\'k', 'Pushti'], 'storage': ['256 GB', '512 GB', '1 TB'], 'ram': ['8 GB', '16 GB', '24 GB']}},
            {'name': 'ASUS ROG Zephyrus G16', 'category': 'ASUS', 'brand': 'ASUS', 'base_price': 35000000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['512 GB', '1 TB', '2 TB'], 'ram': ['16 GB', '32 GB', '64 GB']}},
            {'name': 'ASUS ROG Strix G18', 'category': 'ASUS', 'brand': 'ASUS', 'base_price': 40000000, 'options': {'color': ['Qora'], 'storage': ['1 TB', '2 TB'], 'ram': ['32 GB', '64 GB']}},
            {'name': 'ASUS TUF Gaming A15', 'category': 'ASUS', 'brand': 'ASUS', 'base_price': 18000000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['512 GB', '1 TB'], 'ram': ['16 GB', '32 GB']}},
            {'name': 'ASUS VivoBook 15', 'category': 'ASUS', 'brand': 'ASUS', 'base_price': 8000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k'], 'storage': ['256 GB', '512 GB', '1 TB'], 'ram': ['8 GB', '16 GB']}},
            {'name': 'Lenovo Legion 9i', 'category': 'Lenovo', 'brand': 'Lenovo', 'base_price': 50000000, 'options': {'color': ['Qora'], 'storage': ['1 TB', '2 TB'], 'ram': ['32 GB', '64 GB']}},
            {'name': 'Lenovo Legion 5 Pro', 'category': 'Lenovo', 'brand': 'Lenovo', 'base_price': 22000000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['512 GB', '1 TB'], 'ram': ['16 GB', '32 GB']}},
            {'name': 'Lenovo LOQ 15', 'category': 'Lenovo', 'brand': 'Lenovo', 'base_price': 12000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k'], 'storage': ['256 GB', '512 GB'], 'ram': ['8 GB', '16 GB']}},
            {'name': 'Lenovo IdeaPad 5', 'category': 'Lenovo', 'brand': 'Lenovo', 'base_price': 9000000, 'options': {'color': ['Qora', 'Oq', 'Kulrang'], 'storage': ['256 GB', '512 GB', '1 TB'], 'ram': ['8 GB', '16 GB']}},
            {'name': 'HP Victus 16', 'category': 'HP', 'brand': 'HP', 'base_price': 16000000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['512 GB', '1 TB'], 'ram': ['16 GB', '32 GB']}},
            {'name': 'HP Omen 16', 'category': 'HP', 'brand': 'HP', 'base_price': 28000000, 'options': {'color': ['Qora'], 'storage': ['1 TB', '2 TB'], 'ram': ['32 GB', '64 GB']}},
            {'name': 'HP Pavilion 15', 'category': 'HP', 'brand': 'HP', 'base_price': 9500000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k'], 'storage': ['256 GB', '512 GB'], 'ram': ['8 GB', '16 GB']}},
            {'name': 'Dell XPS 16', 'category': 'Dell', 'brand': 'Dell', 'base_price': 38000000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['512 GB', '1 TB', '2 TB'], 'ram': ['16 GB', '32 GB', '64 GB']}},
            {'name': 'Dell Inspiron 16', 'category': 'Dell', 'brand': 'Dell', 'base_price': 10000000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['256 GB', '512 GB', '1 TB'], 'ram': ['8 GB', '16 GB']}},
            {'name': 'iPad Pro 12.9 M4', 'category': 'Apple iPad', 'brand': 'Apple', 'base_price': 28000000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['256 GB', '512 GB', '1 TB', '2 TB'], 'ram': ['8 GB', '16 GB']}},
            {'name': 'iPad Pro 11 M4', 'category': 'Apple iPad', 'brand': 'Apple', 'base_price': 22000000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['128 GB', '256 GB', '512 GB', '1 TB'], 'ram': ['8 GB', '16 GB']}},
            {'name': 'iPad Air M2', 'category': 'Apple iPad', 'brand': 'Apple', 'base_price': 16000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Yashil', 'Pushti'], 'storage': ['128 GB', '256 GB', '512 GB'], 'ram': ['8 GB', '16 GB']}},
            {'name': 'Samsung Galaxy Tab S9 Ultra', 'category': 'Samsung Galaxy Tab', 'brand': 'Samsung', 'base_price': 18000000, 'options': {'color': ['Qora', 'Oq', 'Yashil'], 'storage': ['256 GB', '512 GB'], 'ram': ['12 GB', '16 GB']}},
            {'name': 'Samsung Galaxy Tab S9+', 'category': 'Samsung Galaxy Tab', 'brand': 'Samsung', 'base_price': 14000000, 'options': {'color': ['Qora', 'Oq'], 'storage': ['128 GB', '256 GB'], 'ram': ['8 GB', '12 GB']}},
            {'name': 'Xiaomi Pad 6 Pro', 'category': 'Xiaomi Pad', 'brand': 'Xiaomi', 'base_price': 7000000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k'], 'storage': ['128 GB', '256 GB', '512 GB'], 'ram': ['8 GB', '12 GB', '16 GB']}},
            {'name': 'AirPods Pro 2', 'category': 'Quloqchinlar', 'brand': 'Apple', 'base_price': 2500000, 'options': {'color': ['Oq'], 'version': ['USB-C', 'Lightning']}},
            {'name': 'AirPods 4', 'category': 'Quloqchinlar', 'brand': 'Apple', 'base_price': 1800000, 'options': {'color': ['Oq'], 'version': ['Standart', 'ANC']}},
            {'name': 'Samsung Galaxy Buds3 Pro', 'category': 'Quloqchinlar', 'brand': 'Samsung', 'base_price': 2200000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k'], 'version': ['Pro', 'Standart']}},
            {'name': 'Sony WH-1000XM5', 'category': 'Quloqchinlar', 'brand': 'Sony', 'base_price': 4500000, 'options': {'color': ['Qora', 'Oq'], 'version': ['Standart', 'Wireless']}},
            {'name': 'Apple Watch Ultra 2', 'category': 'Soatlar', 'brand': 'Apple', 'base_price': 6000000, 'options': {'color': ['Qora', 'Oq'], 'size': ['49 mm', '45 mm']}},
            {'name': 'Apple Watch Series 9', 'category': 'Soatlar', 'brand': 'Apple', 'base_price': 3500000, 'options': {'color': ['Qora', 'Oq', 'Ko\'k', 'Pushti'], 'size': ['41 mm', '45 mm'], 'connectivity': ['GPS', 'GPS + Cellular']}},
            {'name': 'Samsung Galaxy Watch6 Classic', 'category': 'Soatlar', 'brand': 'Samsung', 'base_price': 2800000, 'options': {'color': ['Qora', 'Oq'], 'size': ['43 mm', '47 mm']}},
            {'name': 'Samsung 65" Neo QLED 4K', 'category': 'Samsung TV', 'brand': 'Samsung', 'base_price': 15000000, 'options': {'size': ['65"'], 'resolution': ['4K'], 'refresh_rate': ['120 Hz']}},
            {'name': 'Samsung 55" Crystal UHD', 'category': 'Samsung TV', 'brand': 'Samsung', 'base_price': 7000000, 'options': {'size': ['43"', '50"', '55"', '65"'], 'resolution': ['4K'], 'refresh_rate': ['60 Hz']}},
            {'name': 'LG C3 65" OLED', 'category': 'LG TV', 'brand': 'LG', 'base_price': 18000000, 'options': {'size': ['55"', '65"', '77"'], 'resolution': ['4K'], 'refresh_rate': ['120 Hz']}},
            {'name': 'Sony Bravia XR 65"', 'category': 'Sony TV', 'brand': 'Sony', 'base_price': 16000000, 'options': {'size': ['55"', '65"', '75"'], 'resolution': ['4K'], 'refresh_rate': ['120 Hz']}},
        ]

    def create_product(self, product_info, categories, brands):
        cat_nom = product_info['category']
        category = Kategoriya.objects.filter(nom=cat_nom, is_active=True).first()
        if not category:
            return None
        
        brand = brands.get(product_info['brand'])
        
        base_slug = slugify(product_info['name'])
        slug = base_slug
        counter = 1
        while Mahsulot.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        product = Mahsulot.objects.create(
            nom=product_info['name'],
            slug=slug,
            kategoriya=category,
            brend=brand,
            tavsif=f"{product_info['name']} - zamonaviy va sifatli mahsulot. Tez yetkazish imkoniyati bilan.",
            narx=product_info['base_price'],
            eski_narx=int(product_info['base_price'] * 1.15),
            soni=100,
            is_active=True,
            tavsiya_etilgan=random.choice([True, False]),
            yangi=random.choice([True, False]),
            sotish_soni=random.randint(10, 500),
            reyting=round(random.uniform(3.5, 5.0), 2),
            reyting_soni=random.randint(5, 200),
        )
        return product

    def create_variants(self, product, option_types, product_info):
        options = product_info.get('options', {})
        if not options:
            return 0
        
        option_values_map = {}
        for opt_key, values in options.items():
            option_type = option_types.get(opt_key)
            if not option_type:
                continue
            option_values_map[opt_key] = []
            for val in values:
                ov, _ = OptionValue.objects.get_or_create(
                    option_type=option_type,
                    qiymat=slugify(val).replace('-', '_'),
                    defaults={'nom': val, 'rang_kod': self.get_color_code(val) if opt_key == 'color' else ''}
                )
                option_values_map[opt_key].append(ov)
        
        if not option_values_map:
            return 0
        
        keys = list(option_values_map.keys())
        combinations = self.get_combinations(keys, option_values_map)
        
        variants_created = 0
        for combo in combinations:
            sku = self.generate_sku(product, combo)
            if MahsulotVariant.objects.filter(sku=sku).exists():
                continue
            
            base_price = product.narx
            price_modifier = random.uniform(0.9, 1.3)
            variant_price = int(base_price * price_modifier)
            old_price = int(variant_price * random.uniform(1.05, 1.25))
            stock = random.randint(0, 50)
            
            variant = MahsulotVariant.objects.create(
                mahsulot=product,
                sku=sku,
                narx=variant_price,
                eski_narx=old_price,
                soni=stock,
                is_active=True
            )
            
            for opt_key, ov in combo.items():
                VariantOption.objects.create(variant=variant, option_value=ov)
            
            variants_created += 1
        
        return variants_created

    def get_combinations(self, keys, option_values_map):
        if not keys:
            return [{}]
        
        result = [{}]
        for key in keys:
            new_result = []
            for combo in result:
                for ov in option_values_map[key]:
                    new_combo = combo.copy()
                    new_combo[key] = ov
                    new_result.append(new_combo)
            result = new_result
        
        max_combinations = 100
        if len(result) > max_combinations:
            result = random.sample(result, max_combinations)
        
        return result

    def generate_sku(self, product, combo):
        brand_code = slugify(product.brend.nom if product.brend else 'GEN').upper()[:3]
        model_code = slugify(product.nom).upper()[:8].replace('-', '')
        option_code = ''.join([slugify(str(ov.qiymat)).upper()[:4] for ov in combo.values()])
        return f"{brand_code}-{model_code}-{option_code}"

    def get_color_code(self, color_name):
        color_map = {
            'Qora': '#000000',
            'Oq': '#FFFFFF',
            'Ko\'k': '#0000FF',
            'Qizil': '#FF0000',
            'Yashil': '#008000',
            'Sariq': '#FFFF00',
            'Binafsha': '#800080',
            'Kulrang': '#808080',
            'Jigar': '#B7410E',
            'Pushti': '#FFC0CB',
            'Titanium': '#878681',
        }
        return color_map.get(color_name, '#CCCCCC')
