from django.contrib import admin
from django import forms
from django.db import models
from django.utils.html import format_html
from .models import *
from .forms import MahsulotVariantForm


class VariantOptionInline(admin.TabularInline):
    model = VariantOption
    extra = 1
    autocomplete_fields = ['option_value']


class VariantRasmInline(admin.TabularInline):
    model = VariantRasm
    extra = 1


class MahsulotVariantInline(admin.TabularInline):
    model = MahsulotVariant
    extra = 1
    show_change_link = True


# Override the inline to include nested inlines
class MahsulotVariantInlineWithOptions(admin.TabularInline):
    model = MahsulotVariant
    extra = 1
    show_change_link = True
    autocomplete_fields = []


class MahsulotRasmInline(admin.TabularInline):
    model = MahsulotRasm
    extra = 1


@admin.register(Foydalanuvchi)
class FoydalanuvchiAdmin(admin.ModelAdmin):
    list_display = ['username', 'get_full_name', 'telefon', 'email', 'is_active', 'is_staff', 'created_at']
    list_filter = ['is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'first_name', 'last_name', 'telefon', 'email']
    list_editable = ['is_active']


@admin.register(Kategoriya)
class KategoriyaAdmin(admin.ModelAdmin):
    list_display = ['nom', 'parent', 'daraja', 'is_active', 'created_at']
    list_filter = ['is_active', 'daraja', 'parent']
    search_fields = ['nom']
    prepopulated_fields = {'slug': ('nom',)}
    list_editable = ['is_active']


@admin.register(Brend)
class BrendAdmin(admin.ModelAdmin):
    list_display = ['nom', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['nom']
    prepopulated_fields = {'slug': ('nom',)}
    list_editable = ['is_active']


class MahsulotVariantInline(admin.TabularInline):
    model = MahsulotVariant
    extra = 1
    show_change_link = True
    form = MahsulotVariantForm


@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    list_display = ['nom', 'kategoriya', 'brend', 'narx', 'soni', 'is_active', 'tavsiya_etilgan', 'yangi', 'created_at']
    list_filter = ['kategoriya', 'brend', 'is_active', 'tavsiya_etilgan', 'yangi', 'created_at']
    search_fields = ['nom', 'tavsif', 'xarita_kod']
    prepopulated_fields = {'slug': ('nom',)}
    inlines = [MahsulotRasmInline, MahsulotVariantInline]
    list_editable = ['is_active', 'tavsiya_etilgan', 'yangi']
    readonly_fields = ['ko_rishlar', 'sotish_soni', 'reyting', 'reyting_soni']
    actions = ['activate_products', 'deactivate_products', 'mark_bestseller', 'mark_featured']

    def base_price(self, obj):
        return f"{obj.narx:,.0f} so'm"
    base_price.short_description = 'Baza narx'

    def variants_count(self, obj):
        return obj.variantlar.filter(is_active=True).count()
    variants_count.short_description = 'Variantlar'

    def total_stock(self, obj):
        return sum(v.soni for v in obj.variantlar.all())
    total_stock.short_description = 'Jami stock'

    def activate_products(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, 'Tanlangan mahsulotlar faollashtirildi')
    activate_products.short_description = 'Faollashtirish'

    def deactivate_products(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, 'Tanlangan mahsulotlar nofaollashtirildi')
    deactivate_products.short_description = 'Nofaollashtirish'

    def mark_bestseller(self, request, queryset):
        queryset.update(tavsiya_etilgan=True)
        self.message_user(request, 'Tanlangan mahsulotlar bestseller deb belgilandi')
    mark_bestseller.short_description = 'Bestseller belgilash'

    def mark_featured(self, request, queryset):
        queryset.update(yangi=True)
        self.message_user(request, 'Tanlangan mahsulotlar yangi deb belgilandi')
    mark_featured.short_description = 'Yangi mahsulot belgilash'


@admin.register(MahsulotRasm)
class MahsulotRasmAdmin(admin.ModelAdmin):
    list_display = ['mahsulot', 'asosiy', 'created_at']
    list_filter = ['asosiy', 'created_at']
    search_fields = ['mahsulot__nom']


@admin.register(MahsulotVariant)
class MahsulotVariantAdmin(admin.ModelAdmin):
    list_display = ['mahsulot', 'sku', 'variant_nomi', 'narx', 'eski_narx', 'chegirma_foiz', 'soni', 'mavjud', 'is_active']
    list_filter = ['mahsulot__kategoriya', 'mahsulot__brend', 'is_active']
    search_fields = ['mahsulot__nom', 'sku']
    list_editable = ['narx', 'eski_narx', 'soni', 'is_active']
    form = MahsulotVariantForm
    inlines = [VariantOptionInline, VariantRasmInline]
    actions = ['activate_variants', 'deactivate_variants', 'update_stock']

    def variant_nomi(self, obj):
        return obj.variant_nomi
    variant_nomi.short_description = 'Variant'

    def mavjud(self, obj):
        return obj.mavjud
    mavjud.short_description = 'Mavjud'
    mavjud.boolean = True

    def activate_variants(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, 'Variantlar faollashtirildi')
    activate_variants.short_description = 'Faollashtirish'

    def deactivate_variants(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, 'Variantlar nofaollashtirildi')
    deactivate_variants.short_description = 'Nofaollashtirish'

    def update_stock(self, request, queryset):
        for variant in queryset:
            variant.soni = 100
            variant.save(update_fields=['soni'])
        self.message_user(request, 'Stock 100 ga yangilandi')
    update_stock.short_description = 'Stockni 100 ga yangilash'


@admin.register(OptionType)
class OptionTypeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'kalit', 'turi', 'tartib', 'is_active']
    list_filter = ['turi', 'is_active']
    search_fields = ['nom', 'kalit']
    list_editable = ['tartib', 'is_active']


@admin.register(OptionValue)
class OptionValueAdmin(admin.ModelAdmin):
    list_display = ['option_type', 'nom', 'qiymat', 'rang_kod', 'tartib']
    list_filter = ['option_type']
    search_fields = ['nom', 'qiymat']
    list_editable = ['tartib']
    autocomplete_fields = ['option_type']


@admin.register(VariantOption)
class VariantOptionAdmin(admin.ModelAdmin):
    list_display = ['variant', 'option_value']
    list_filter = ['option_value__option_type']
    search_fields = ['variant__mahsulot__nom', 'option_value__nom']
    autocomplete_fields = ['variant', 'option_value']


@admin.register(VariantRasm)
class VariantRasmAdmin(admin.ModelAdmin):
    list_display = ['variant', 'asosiy', 'created_at']
    list_filter = ['asosiy', 'created_at']
    search_fields = ['variant__mahsulot__nom']


@admin.register(ViloyatRaioni)
class ViloyatRaioniAdmin(admin.ModelAdmin):
    list_display = ['viloyat', 'raion', 'yetkazish_narxi', 'kunlar', 'is_active']
    list_filter = ['viloyat', 'is_active']
    search_fields = ['viloyat', 'raion']
    list_editable = ['is_active', 'yetkazish_narxi', 'kunlar']


@admin.register(FoydalanuvchiManzil)
class FoydalanuvchiManzilAdmin(admin.ModelAdmin):
    list_display = ['user', 'ism', 'familiya', 'viloyat', 'raion', 'asosiy']
    list_filter = ['viloyat', 'asosiy']
    search_fields = ['user__username', 'ism', 'familiya', 'telefon']


class BuyurtmaMahsulotInline(admin.TabularInline):
    model = BuyurtmaMahsulot
    extra = 0
    readonly_fields = ['mahsulot', 'variant', 'narx', 'miqdor', 'jami']


class TolomInline(admin.TabularInline):
    model = Tolom
    extra = 0
    readonly_fields = ['tolov_turi', 'summa', 'tranzaksiya_id', 'holat']


class ChekInline(admin.TabularInline):
    model = Chek
    extra = 0
    readonly_fields = ['summa', 'holat', 'izoh', 'created_at']


@admin.register(Buyurtma)
class BuyurtmaAdmin(admin.ModelAdmin):
    list_display = ['buyurtma_raqami', 'ism', 'familiya', 'holat', 'tolov_turi', 'jami', 'created_at']
    list_filter = ['holat', 'tolov_turi', 'created_at']
    search_fields = ['buyurtma_raqami', 'ism', 'familiya', 'telefon']
    inlines = [BuyurtmaMahsulotInline, TolomInline, ChekInline]
    readonly_fields = ['buyurtma_raqami', 'created_at', 'updated_at', 'qr_kod', 'qr_kod_yaratildi']
    list_editable = ['holat']

    actions = ['tasdiqlash', 'rad_etish', 'qr_kod_yaratish']

    def tasdiqlash(self, request, queryset):
        for buyurtma in queryset:
            buyurtma.holat = 'tasdiqlandi'
            buyurtma.save(update_fields=['holat'])
            if not buyurtma.qr_kod:
                buyurtma.generate_qr_code()
        self.message_user(request, 'Buyurtmalar tasdiqlandi va QR kodlar yaratildi')

    def rad_etish(self, request, queryset):
        queryset.update(holat='bekor_qilindi')
        self.message_user(request, 'Buyurtmalar rad etildi')

    def qr_kod_yaratish(self, request, queryset):
        for buyurtma in queryset:
            if not buyurtma.qr_kod:
                buyurtma.generate_qr_code()
        self.message_user(request, 'QR kodlar yaratildi')

    tasdiqlash.short_description = 'Tanlangan buyurtmalarni tasdiqlash'
    rad_etish.short_description = 'Tanlangan buyurtmalarni rad etish'
    qr_kod_yaratish.short_description = 'QR kod yaratish'


@admin.register(Tolom)
class TolomAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyurtma', 'tolov_turi', 'summa', 'holat', 'created_at']
    list_filter = ['tolov_turi', 'holat', 'created_at']
    search_fields = ['buyurtma__buyurtma_raqami', 'tranzaksiya_id']


@admin.register(Aktsiya)
class AktsiyaAdmin(admin.ModelAdmin):
    list_display = ['nom', 'boshlanish', 'tugash', 'chegirma_foiz', 'chegirma_summa', 'is_active']
    list_filter = ['is_active', 'boshlanish', 'tugash']
    search_fields = ['nom']
    prepopulated_fields = {'slug': ('nom',)}
    list_editable = ['is_active']
    readonly_fields = ['rasm_preview']

    def rasm_preview(self, obj):
        if obj.rasm:
            try:
                return format_html('<img src="{}" style="max-height: 200px; max-width: 200px; border-radius: 8px;">', obj.rasm.url)
            except Exception:
                return 'Rasmni yuklashda xatolik'
        return "Rasm yo'q"
    rasm_preview.short_description = 'Rasm'


@admin.register(Kupon)
class KuponAdmin(admin.ModelAdmin):
    list_display = ['kod', 'nom', 'turi', 'qiymat', 'foydalanildi', 'ishlamatdan_soni', 'boshlanish', 'tugash', 'is_active']
    list_filter = ['turi', 'is_active', 'boshlanish', 'tugash']
    search_fields = ['kod', 'nom']
    list_editable = ['is_active']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['nom', 'pozitsiya', 'tartib', 'is_active', 'created_at']
    list_filter = ['pozitsiya', 'is_active']
    search_fields = ['nom']
    list_editable = ['tartib', 'is_active']
    readonly_fields = ['rasm_preview']

    def rasm_preview(self, obj):
        if obj.rasm:
            try:
                return format_html('<img src="{}" style="max-height: 200px; max-width: 200px; border-radius: 8px;">', obj.rasm.url)
            except Exception:
                return 'Rasmni yuklashda xatolik'
        return "Rasm yo'q"
    rasm_preview.short_description = 'Rasm'


@admin.register(Fikr)
class FikrAdmin(admin.ModelAdmin):
    list_display = ['mahsulot', 'user', 'reyting', 'is_active', 'created_at']
    list_filter = ['reyting', 'is_active', 'created_at']
    search_fields = ['mahsulot__nom', 'user__username', 'izoh']
    list_editable = ['is_active']


@admin.register(Istaknafar)
class IstaknafarAdmin(admin.ModelAdmin):
    list_display = ['user', 'mahsulot', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'mahsulot__nom']


@admin.register(Taqqoslash)
class TaqqoslashAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['email']
    list_editable = ['is_active']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['savol', 'tartib', 'is_active']
    list_filter = ['is_active']
    search_fields = ['savol', 'javob']
    list_editable = ['is_active', 'tartib']


@admin.register(SaytSozlamalar)
class SaytSozlamalarAdmin(admin.ModelAdmin):
    list_display = ['kalit', 'qiymat', 'updated_at']
    search_fields = ['kalit', 'qiymat']


@admin.register(KaroshaTarixi)
class KaroshaTarixiAdmin(admin.ModelAdmin):
    list_display = ['user', 'harakat', 'ip', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'harakat']
    readonly_fields = ['user', 'harakat', 'ip', 'user_agent', 'created_at']


@admin.register(Savatcha)
class SavatchaAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'sessiya_id', 'jami', 'soni', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'sessiya_id']


@admin.register(SavatchaMahsulot)
class SavatchaMahsulotAdmin(admin.ModelAdmin):
    list_display = ['savatcha', 'mahsulot', 'variant', 'miqdor', 'jami']
    list_filter = ['mahsulot__kategoriya']
    search_fields = ['mahsulot__nom', 'savatcha__id']


@admin.register(DemoKarta)
class DemoKartaAdmin(admin.ModelAdmin):
    list_display = ['nom', 'tur', 'karta_raqami', 'balans', 'holat', 'created_at']
    list_filter = ['tur', 'holat', 'created_at']
    search_fields = ['nom', 'karta_raqami']
    list_editable = ['holat', 'balans']


@admin.register(Chek)
class ChekAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyurtma', 'demo_karta', 'summa', 'holat', 'izoh', 'created_at']
    list_filter = ['holat', 'created_at']
    search_fields = ['buyurtma__buyurtma_raqami', 'demo_karta__karta_raqami']
    list_editable = ['holat', 'izoh']
    readonly_fields = ['buyurtma', 'demo_karta', 'summa', 'created_at']


@admin.register(SaytMalumotlari)
class SaytMalumotlariAdmin(admin.ModelAdmin):
    list_display = ['nom', 'updated_at']
    search_fields = ['nom', 'qiymat']
    readonly_fields = ['updated_at']
