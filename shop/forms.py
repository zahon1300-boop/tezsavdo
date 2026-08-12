from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Foydalanuvchi, FoydalanuvchiManzil, Fikr, Buyurtma


class RoyxatanOtishForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefon = forms.CharField(max_length=20, required=False)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Foydalanuvchi
        fields = ['username', 'first_name', 'last_name', 'email', 'telefon', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.telefon = self.cleaned_data['telefon']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class KirishForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    eslab_qol = forms.BooleanField(required=False)


class FoydalanuvchiProfilForm(forms.ModelForm):
    class Meta:
        model = Foydalanuvchi
        fields = ['first_name', 'last_name', 'email', 'telefon', 'tugilgan_sana', 'avatar']
        widgets = {
            'tugilgan_sana': forms.DateInput(attrs={'type': 'date'}),
        }


class ManzilForm(forms.ModelForm):
    class Meta:
        model = FoydalanuvchiManzil
        fields = ['ism', 'familiya', 'telefon', 'viloyat', 'raion', 'manzil', 'binolar', 'kvartira', 'pochta_kod', 'izoh', 'asosiy']


class FikrForm(forms.ModelForm):
    class Meta:
        model = Fikr
        fields = ['reyting', 'izoh']
        widgets = {
            'izoh': forms.Textarea(attrs={'rows': 4}),
        }


class ParolOzgartirishForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Eski parol'
        self.fields['new_password1'].label = 'Yangi parol'
        self.fields['new_password2'].label = 'Yangi parolni takrorlang'


class BuyurtmaForm(forms.Form):
    ism = forms.CharField(max_length=100)
    familiya = forms.CharField(max_length=100)
    telefon = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    viloyat = forms.CharField(max_length=100)
    raion = forms.CharField(max_length=100)
    manzil = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'rows': 2}))
    binolar = forms.CharField(max_length=50, required=False)
    kvartira = forms.CharField(max_length=50, required=False)
    pochta_kod = forms.CharField(max_length=10, required=False)
    izoh = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    tolov_turi = forms.ChoiceField(choices=Buyurtma.TOLOM_TURLARI)
    manzil_id = forms.IntegerField(required=False)
