from rest_framework import serializers
from .models import *


class KategoriyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategoriya
        fields = ['id', 'nom', 'slug', 'rasm', 'parent', 'daraja', 'is_active']


class BrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brend
        fields = ['id', 'nom', 'slug', 'logo', 'tavsif', 'is_active']


class MahsulotVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = MahsulotVariant
        fields = ['id', 'rang', 'rang_kod', 'hajm', 'narx', 'soni']


class MahsulotRasmSerializer(serializers.ModelSerializer):
    class Meta:
        model = MahsulotRasm
        fields = ['id', 'rasm', 'asosiy']


class MahsulotSerializer(serializers.ModelSerializer):
    kategoriya = KategoriyaSerializer(read_only=True)
    brend = BrendSerializer(read_only=True)
    rasmlar = MahsulotRasmSerializer(many=True, read_only=True)
    variantlar = MahsulotVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Mahsulot
        fields = ['id', 'nom', 'slug', 'kategoriya', 'brend', 'tavsif', 'narx', 'eski_narx',
                  'chegirma_foiz', 'soni', 'xarita_kod', 'is_active', 'tavsiya_etilgan',
                  'yangi', 'oxirgi', 'ko_rishlar', 'sotish_soni', 'reyting', 'reyting_soni',
                  'rasmlar', 'variantlar', 'created_at']


class BuyurtmaMahsulotSerializer(serializers.ModelSerializer):
    mahsulot = MahsulotSerializer(read_only=True)

    class Meta:
        model = BuyurtmaMahsulot
        fields = ['id', 'mahsulot', 'variant', 'narx', 'miqdor', 'jami']


class BuyurtmaSerializer(serializers.ModelSerializer):
    mahsulotlar = BuyurtmaMahsulotSerializer(many=True, read_only=True)

    class Meta:
        model = Buyurtma
        fields = ['id', 'buyurtma_raqami', 'ism', 'familiya', 'telefon', 'email',
                  'viloyat', 'raion', 'manzil', 'holat', 'tolov_turi', 'jami', 'created_at']
