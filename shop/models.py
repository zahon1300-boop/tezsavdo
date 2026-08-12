from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone


class Foydalanuvchi(AbstractUser):
    telefon = models.CharField(max_length=20, blank=True)
    tugilgan_sana = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return self.get_full_name() or self.username


class Kategoriya(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    rasm = models.ImageField(upload_to='kategoriyalar/', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='bolalari')
    daraja = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        ordering = ['daraja', 'nom']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Brend(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='brendlar/', null=True, blank=True)
    tavsif = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Brend'
        verbose_name_plural = 'Brendlar'
        ordering = ['nom']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Mahsulot(models.Model):
    nom = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE, related_name='mahsulotlar')
    brend = models.ForeignKey(Brend, on_delete=models.CASCADE, related_name='mahsulotlar', null=True, blank=True)
    tavsif = models.TextField(blank=True)
    narx = models.DecimalField(max_digits=12, decimal_places=2)
    eski_narx = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    chegirma_foiz = models.PositiveIntegerField(default=0)
    soni = models.PositiveIntegerField(default=0)
    xarita_kod = models.CharField(max_length=100, blank=True)
    ogirlik = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    uzunlik = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    kenglik = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    balandlik = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    tavsiya_etilgan = models.BooleanField(default=False)
    yangi = models.BooleanField(default=False)
    oxirgi = models.BooleanField(default=False)
    ko_rishlar = models.PositiveIntegerField(default=0)
    sotish_soni = models.PositiveIntegerField(default=0)
    reyting = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    reyting_soni = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', '-created_at']),
            models.Index(fields=['kategoriya', 'is_active']),
            models.Index(fields=['brend', 'is_active']),
            models.Index(fields=['-sotish_soni']),
            models.Index(fields=['-reyting']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        if self.eski_narx and self.eski_narx > self.narx:
            self.chegirma_foiz = int((self.eski_narx - self.narx) / self.eski_narx * 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def starting_price(self):
        min_variant = self.variantlar.filter(is_active=True, soni__gt=0).order_by('narx').first()
        if min_variant:
            return min_variant.narx
        return self.narx

    @property
    def has_variants(self):
        return self.variantlar.filter(is_active=True).exists()

    @property
    def default_variant_id(self):
        v = self.variantlar.filter(is_active=True, soni__gt=0).first()
        return v.id if v else None


class MahsulotRasm(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE, related_name='rasmlar')
    rasm = models.ImageField(upload_to='mahsulotlar/')
    asosiy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mahsulot rasmi'
        verbose_name_plural = 'Mahsulot rasmlari'
        ordering = ['-asosiy', 'created_at']

    def __str__(self):
        return f"{self.mahsulot.nom} - {self.id}"


class OptionType(models.Model):
    TUR_TURLARI = [
        ('color', 'Rang'),
        ('text', 'Matn'),
        ('number', 'Raqam'),
        ('boolean', 'Mantiqiy'),
    ]

    nom = models.CharField(max_length=50, unique=True)
    kalit = models.CharField(max_length=50, unique=True)
    turi = models.CharField(max_length=20, choices=TUR_TURLARI, default='text')
    tartib = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Variant turi'
        verbose_name_plural = 'Variant turlari'
        ordering = ['tartib', 'nom']

    def __str__(self):
        return self.nom


class OptionValue(models.Model):
    option_type = models.ForeignKey(OptionType, on_delete=models.CASCADE, related_name='qiymatlar')
    nom = models.CharField(max_length=100)
    qiymat = models.CharField(max_length=100)
    rang_kod = models.CharField(max_length=10, blank=True, help_text='Rang uchun HEX kod')
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Variant qiymati'
        verbose_name_plural = 'Variant qiymatlari'
        ordering = ['tartib', 'nom']
        unique_together = ['option_type', 'qiymat']

    def __str__(self):
        return f"{self.option_type.nom}: {self.nom}"


class MahsulotVariant(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE, related_name='variantlar')
    sku = models.CharField(max_length=100, blank=True)
    narx = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    eski_narx = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    soni = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='variantlar/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Mahsulot varianti'
        verbose_name_plural = 'Mahsulot variantlari'
        ordering = ['id']
        indexes = [
            models.Index(fields=['mahsulot', 'is_active']),
            models.Index(fields=['sku']),
            models.Index(fields=['soni']),
        ]

    def __str__(self):
        options = self.variant_ops.all().select_related('option_value__option_type')
        parts = [f"{ov.option_value.option_type.nom}: {ov.option_value.nom}" for ov in options]
        return f"{self.mahsulot.nom} - {', '.join(parts)}"

    @property
    def chegirma_foiz(self):
        if self.eski_narx and self.eski_narx > self.narx:
            return int((self.eski_narx - self.narx) / self.eski_narx * 100)
        return 0

    @property
    def mavjud(self):
        return self.soni > 0

    @property
    def variant_nomi(self):
        options = self.variant_ops.all().select_related('option_value__option_type')
        parts = [ov.option_value.nom for ov in options]
        return ' / '.join(parts)


class VariantOption(models.Model):
    variant = models.ForeignKey(MahsulotVariant, on_delete=models.CASCADE, related_name='variant_ops')
    option_value = models.ForeignKey(OptionValue, on_delete=models.CASCADE, related_name='variant_ops')

    class Meta:
        verbose_name = 'Variant opsiyasi'
        verbose_name_plural = 'Variant opsiyalari'
        unique_together = ['variant', 'option_value']
        ordering = ['option_value__option_type__tartib', 'option_value__tartib']

    def __str__(self):
        return f"{self.variant} - {self.option_value}"


class VariantRasm(models.Model):
    variant = models.ForeignKey(MahsulotVariant, on_delete=models.CASCADE, related_name='rasmlar')
    rasm = models.ImageField(upload_to='variantlar/rasmlar/')
    asosiy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Variant rasmi'
        verbose_name_plural = 'Variant rasmlari'
        ordering = ['-asosiy', 'created_at']

    def __str__(self):
        return f"{self.variant} - {self.id}"


class ViloyatRaioni(models.Model):
    viloyat = models.CharField(max_length=100)
    raion = models.CharField(max_length=100)
    pochta_kod = models.CharField(max_length=10, blank=True)
    yetkazish_narxi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    kunlar = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Viloyat/raion'
        verbose_name_plural = 'Viloyat/raionlar'
        unique_together = ['viloyat', 'raion']
        ordering = ['viloyat', 'raion']

    def __str__(self):
        return f"{self.viloyat}, {self.raion}"


class FoydalanuvchiManzil(models.Model):
    user = models.ForeignKey(Foydalanuvchi, on_delete=models.CASCADE, related_name='manzillar')
    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)
    viloyat = models.CharField(max_length=100)
    raion = models.CharField(max_length=100)
    manzil = models.CharField(max_length=255)
    binolar = models.CharField(max_length=50, blank=True)
    kvartira = models.CharField(max_length=50, blank=True)
    pochta_kod = models.CharField(max_length=10, blank=True)
    izoh = models.TextField(blank=True)
    asosiy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Foydalanuvchi manzili'
        verbose_name_plural = 'Foydalanuvchi manzillari'
        ordering = ['-asosiy', '-created_at']

    def __str__(self):
        return f"{self.ism} {self.familiya} - {self.viloyat}"


class Savatcha(models.Model):
    user = models.ForeignKey(Foydalanuvchi, on_delete=models.CASCADE, related_name='savatchalar', null=True, blank=True)
    sessiya_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Savatcha'
        verbose_name_plural = 'Savatchalar'

    def __str__(self):
        return f"Savatcha #{self.id}"

    @property
    def jami(self):
        return sum(item.jami for item in self.mahsulotlar.all())

    @property
    def soni(self):
        return sum(item.miqdor for item in self.mahsulotlar.all())


class SavatchaMahsulot(models.Model):
    savatcha = models.ForeignKey(Savatcha, on_delete=models.CASCADE, related_name='mahsulotlar')
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)
    variant = models.ForeignKey(MahsulotVariant, on_delete=models.CASCADE, null=True, blank=True)
    miqdor = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Savatcha mahsuloti'
        verbose_name_plural = 'Savatcha mahsulotlari'
        unique_together = ['savatcha', 'mahsulot', 'variant']

    def __str__(self):
        return f"{self.mahsulot.nom} x{self.miqdor}"

    @property
    def jami(self):
        price = self.variant.narx if self.variant and self.variant.narx else self.mahsulot.narx
        return price * self.miqdor

    @property
    def unit_price(self):
        return self.variant.narx if self.variant and self.variant.narx else self.mahsulot.narx


class Buyurtma(models.Model):
    HOLAT_TURLARI = [
        ('kutilmoqda', 'Kutilmoqda'),
        ('tasdiqlandi', 'Tasdiqlandi'),
        ('yigilmoqda', "Yig'ilmoqda"),
        ('jonatilgan', 'Yuborilgan'),
        ('yetkazildi', 'Yetkazildi'),
        ('bekor_qilindi', 'Bekor qilindi'),
        ('qr_kutilmoqda', 'QR kod kutilmoqda'),
        ('qr_tasdiqlandi', 'QR tasdiqlandi'),
    ]

    TOLOM_TURLARI = [
        ('naqd', 'Naqd'),
        ('karta', 'Karta'),
        ('click', 'Click'),
        ('payme', 'PayMe'),
    ]

    user = models.ForeignKey(Foydalanuvchi, on_delete=models.CASCADE, related_name='buyurtmalar', null=True, blank=True)
    buyurtma_raqami = models.CharField(max_length=50, unique=True)
    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    viloyat = models.CharField(max_length=100)
    raion = models.CharField(max_length=100)
    manzil = models.CharField(max_length=255)
    binolar = models.CharField(max_length=50, blank=True)
    kvartira = models.CharField(max_length=50, blank=True)
    pochta_kod = models.CharField(max_length=10, blank=True)
    izoh = models.TextField(blank=True)
    holat = models.CharField(max_length=20, choices=HOLAT_TURLARI, default='kutilmoqda')
    tolov_turi = models.CharField(max_length=20, choices=TOLOM_TURLARI, default='naqd')
    yetkazish_narxi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    chegirma = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    jami = models.DecimalField(max_digits=12, decimal_places=2)
    ip = models.GenericIPAddressField(null=True, blank=True)
    qr_kod = models.ImageField(upload_to='qr_kodlar/', null=True, blank=True)
    qr_kod_yaratildi = models.DateTimeField(null=True, blank=True)
    baholandi = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
        ordering = ['-created_at']

    def __str__(self):
        return f"Buyurtma #{self.buyurtma_raqami}"

    def generate_qr_code(self):
        import qrcode
        import json
        from django.core.files.base import ContentFile
        from io import BytesIO

        items = []
        for item in self.mahsulotlar.all():
            items.append({
                'id': item.mahsulot.id,
                'nom': item.mahsulot.nom,
                'variant': item.variant.variant_nomi if item.variant else '',
                'miqdor': item.miqdor,
                'narx': str(item.narx),
                'jami': str(item.jami),
            })

        qr_data = {
            'buyurtma_raqami': self.buyurtma_raqami,
            'ism': self.ism,
            'familiya': self.familiya,
            'telefon': self.telefon,
            'tolov_turi': self.get_tolov_turi_display(),
            'jami': str(self.jami),
            'mahsulotlar': items,
            'manzil': f"{self.viloyat}, {self.raion}",
        }

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(json.dumps(qr_data, ensure_ascii=False))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'qr_{self.buyurtma_raqami}.png'
        self.qr_kod.save(filename, ContentFile(buffer.getvalue()), save=False)
        self.qr_kod_yaratildi = timezone.now()
        self.save()


class BuyurtmaMahsulot(models.Model):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE, related_name='mahsulotlar')
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)
    variant = models.ForeignKey(MahsulotVariant, on_delete=models.CASCADE, null=True, blank=True)
    narx = models.DecimalField(max_digits=12, decimal_places=2)
    miqdor = models.PositiveIntegerField(default=1)
    jami = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Buyurtma mahsuloti'
        verbose_name_plural = 'Buyurtma mahsulotlari'

    def __str__(self):
        return f"{self.mahsulot.nom} x{self.miqdor}"


class Tolom(models.Model):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE, related_name='tolovlar')
    tolov_turi = models.CharField(max_length=20)
    summa = models.DecimalField(max_digits=12, decimal_places=2)
    tranzaksiya_id = models.CharField(max_length=100, blank=True)
    demo_karta = models.ForeignKey('DemoKarta', on_delete=models.SET_NULL, null=True, blank=True, related_name='tolovlar')
    holat = models.CharField(max_length=20, default='kutilmoqda')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tolov'
        verbose_name_plural = 'Tolovlar'

    def __str__(self):
        return f"Tolov #{self.id} - {self.buyurtma.buyurtma_raqami}"


class Aktsiya(models.Model):
    nom = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tavsif = models.TextField(blank=True)
    boshlanish = models.DateTimeField()
    tugash = models.DateTimeField()
    chegirma_foiz = models.PositiveIntegerField(default=0)
    chegirma_summa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rasm = models.ImageField(upload_to='aktsiyalar/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Aktsiya'
        verbose_name_plural = 'Aktsiyalar'
        ordering = ['-boshlanish']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Kupon(models.Model):
    kod = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=200, blank=True)
    tavsif = models.TextField(blank=True)
    turi = models.CharField(max_length=20, choices=[('foiz', 'Foiz'), ('summa', 'Summa')], default='foiz')
    qiymat = models.DecimalField(max_digits=10, decimal_places=2)
    minimal_tovar = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    maksimal_chegirma = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    foydalanuvchi = models.ForeignKey(Foydalanuvchi, on_delete=models.CASCADE, null=True, blank=True, related_name='kuponlar')
    ishlamatdan_soni = models.PositiveIntegerField(default=1)
    foydalanildi = models.PositiveIntegerField(default=0)
    boshlanish = models.DateTimeField()
    tugash = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Kupon'
        verbose_name_plural = 'Kuponlar'
        ordering = ['-created_at']

    def __str__(self):
        return self.kod


class Banner(models.Model):
    nom = models.CharField(max_length=200)
    rasm = models.ImageField(upload_to='bannerlar/')
    havola = models.URLField(blank=True)
    matn = models.CharField(max_length=500, blank=True)
    tugma_matni = models.CharField(max_length=100, blank=True)
    pozitsiya = models.CharField(max_length=20, choices=[
        ('bosh', 'Bosh sahifa'),
        ('katalog', 'Katalog'),
        ('chegirma', 'Chegirma'),
    ], default='bosh')
    tartib = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    boshlanish = models.DateTimeField(null=True, blank=True)
    tugash = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Bannerlar'
        ordering = ['tartib', '-created_at']

    def __str__(self):
        return self.nom


class Fikr(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE, related_name='fikrlar')
    user = models.ForeignKey(Foydalanuvchi, on_delete=models.CASCADE, related_name='fikrlar')
    reyting = models.PositiveIntegerField(default=5)
    izoh = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Fikr'
        verbose_name_plural = 'Fikrlar'
        unique_together = ['mahsulot', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.mahsulot.nom}"


class Istaknafar(models.Model):
    user = models.ForeignKey(Foydalanuvchi, on_delete=models.CASCADE, related_name='istaknafarlar')
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Istaknafar'
        verbose_name_plural = 'Istaknafarlar'
        unique_together = ['user', 'mahsulot']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.mahsulot.nom}"


class Taqqoslash(models.Model):
    user = models.ForeignKey(Foydalanuvchi, on_delete=models.CASCADE, related_name='taqqoshlar')
    mahsulotlar = models.ManyToManyField(Mahsulot, related_name='taqqoshlar')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Taqqoslash'
        verbose_name_plural = 'Taqqoshlar'
        ordering = ['-created_at']

    def __str__(self):
        return f"Taqqoslash #{self.id}"


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletterlar'
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class FAQ(models.Model):
    savol = models.CharField(max_length=255)
    javob = models.TextField()
    tartib = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQlar'
        ordering = ['tartib']

    def __str__(self):
        return self.savol


class SaytSozlamalar(models.Model):
    kalit = models.CharField(max_length=100, unique=True)
    qiymat = models.TextField()
    tavsif = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sayt sozlamasi'
        verbose_name_plural = 'Sayt sozlamalari'

    def __str__(self):
        return self.kalit


class KaroshaTarixi(models.Model):
    user = models.ForeignKey(Foydalanuvchi, on_delete=models.CASCADE, null=True, blank=True, related_name='faoliyatlar')
    harakat = models.CharField(max_length=255)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Faoliyat tarixi'
        verbose_name_plural = 'Faoliyat tarixlari'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.harakat}"


class SaytMalumotlari(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    qiymat = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sayt ma'lumoti"
        verbose_name_plural = "Sayt ma'lumotlari"

    def __str__(self):
        return self.nom


class DemoKarta(models.Model):
    TUR_TURLARI = [
        ('uzcard', 'UzCard'),
        ('humo', 'Humo'),
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
    ]

    HOLAT_TURLARI = [
        ('faol', 'Faol'),
        ('nofaol', 'Nofaol'),
    ]

    nom = models.CharField(max_length=100, help_text='Masalan: Demo karta 1')
    tur = models.CharField(max_length=20, choices=TUR_TURLARI)
    karta_raqami = models.CharField(max_length=20, unique=True, help_text='Masalan: 8600 1234 5678 9012')
    amal_qilish_muddati = models.CharField(max_length=7, help_text='MM/YY')
    balans = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    holat = models.CharField(max_length=10, choices=HOLAT_TURLARI, default='faol')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Demo karta'
        verbose_name_plural = 'Demo kartalar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nom} ({self.get_tur_display()}) - {self.karta_raqami}"


class Chek(models.Model):
    HOLAT_TURLARI = [
        ('kutilmoqda', 'Kutilmoqda'),
        ('tasdiqlandi', 'Tasdiqlandi'),
        ('rad_etildi', 'Rad etildi'),
    ]

    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE, related_name='cheklari')
    demo_karta = models.ForeignKey(DemoKarta, on_delete=models.SET_NULL, null=True, blank=True, related_name='cheklari')
    summa = models.DecimalField(max_digits=12, decimal_places=2)
    holat = models.CharField(max_length=20, choices=HOLAT_TURLARI, default='kutilmoqda')
    izoh = models.TextField(blank=True, help_text='Admin izohi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Chek'
        verbose_name_plural = 'Cheklar'
        ordering = ['-created_at']

    def __str__(self):
        return f"Chek #{self.id} - {self.buyurtma.buyurtma_raqami}"
