from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count, Avg, Sum
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from decimal import Decimal
import json
import uuid

from .models import *
from .forms import *


def index(request):
    yangi_mahsulotlar = Mahsulot.objects.filter(yangi=True, is_active=True).prefetch_related('variantlar', 'rasmlar')[:8]
    mashhur_mahsulotlar = Mahsulot.objects.filter(is_active=True).order_by('-sotish_soni').prefetch_related('variantlar', 'rasmlar')[:8]
    oxirgi_mahsulotlar = Mahsulot.objects.filter(oxirgi=True, is_active=True).prefetch_related('variantlar', 'rasmlar')[:8]
    kategoriyalar = Kategoriya.objects.filter(parent__isnull=True, is_active=True)[:24]
    bannerlar = Banner.objects.filter(is_active=True, pozitsiya='bosh').order_by('tartib')[:3]
    aktsiyalar = Aktsiya.objects.filter(is_active=True)[:3]

    context = {
        'yangi_mahsulotlar': yangi_mahsulotlar,
        'mashhur_mahsulotlar': mashhur_mahsulotlar,
        'oxirgi_mahsulotlar': oxirgi_mahsulotlar,
        'kategoriyalar': kategoriyalar,
        'bannerlar': bannerlar,
        'aktsiyalar': aktsiyalar,
    }
    return render(request, 'index.html', context)


def mahsulotlar(request):
    mahsulotlar = Mahsulot.objects.filter(is_active=True)
    kategoriyalar = Kategoriya.objects.filter(is_active=True)
    brendlar = Brend.objects.filter(is_active=True)

    kategoriya_id = request.GET.get('kategoriya')
    brend_id = request.GET.get('brend')
    narx_min = request.GET.get('narx_min')
    narx_max = request.GET.get('narx_max')
    reyting = request.GET.get('reyting')
    qidiruv = request.GET.get('qidiruv')
    tartiblash = request.GET.get('tartiblash', 'yangi')

    if kategoriya_id:
        mahsulotlar = mahsulotlar.filter(kategoriya_id=kategoriya_id)
    if brend_id:
        mahsulotlar = mahsulotlar.filter(brend_id=brend_id)
    if narx_min:
        mahsulotlar = mahsulotlar.filter(narx__gte=narx_min)
    if narx_max:
        mahsulotlar = mahsulotlar.filter(narx__lte=narx_max)
    if reyting:
        mahsulotlar = mahsulotlar.filter(reyting__gte=reyting)
    if qidiruv:
        mahsulotlar = mahsulotlar.filter(
            Q(nom__icontains=qidiruv) | Q(tavsif__icontains=qidiruv)
        )

    if tartiblash == 'narx_arzon':
        mahsulotlar = mahsulotlar.order_by('narx')
    elif tartiblash == 'narx_qimmat':
        mahsulotlar = mahsulotlar.order_by('-narx')
    elif tartiblash == 'reyting':
        mahsulotlar = mahsulotlar.order_by('-reyting')
    elif tartiblash == 'sotish':
        mahsulotlar = mahsulotlar.order_by('-sotish_soni')
    else:
        mahsulotlar = mahsulotlar.order_by('-created_at')

    paginator = Paginator(mahsulotlar, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'kategoriyalar': kategoriyalar,
        'brendlar': brendlar,
    }
    return render(request, 'mahsulotlar.html', context)


def mahsulot_detali(request, slug):
    mahsulot = get_object_or_404(Mahsulot, slug=slug, is_active=True)
    mahsulot.ko_rishlar += 1
    mahsulot.save(update_fields=['ko_rishlar'])

    fikrlar = mahsulot.fikrlar.filter(is_active=True)
    ortacha_reyting = fikrlar.aggregate(Avg('reyting'))['reyting__avg'] or 0

    bog_liq_mahsulotlar = Mahsulot.objects.filter(
        kategoriya=mahsulot.kategoriya, is_active=True
    ).exclude(id=mahsulot.id)[:4]

    variantlar = mahsulot.variantlar.filter(is_active=True).prefetch_related(
        'variant_ops__option_value__option_type'
    )

    variant_options = {}
    for variant in variantlar:
        for vo in variant.variant_ops.all():
            ot = vo.option_value.option_type
            ov = vo.option_value
            if ot.kalit not in variant_options:
                variant_options[ot.kalit] = {
                    'name': ot.nom,
                    'type': ot.turi,
                    'values': []
                }
            if ov.id not in [v['id'] for v in variant_options[ot.kalit]['values']]:
                variant_options[ot.kalit]['values'].append({
                    'id': ov.id,
                    'name': ov.nom,
                    'value': ov.qiymat,
                    'color_code': ov.rang_kod,
                    'variants': []
                })
            for v in variant_options[ot.kalit]['values']:
                if v['id'] == ov.id:
                    v['variants'].append({
                        'id': variant.id,
                        'price': float(variant.narx),
                        'old_price': float(variant.eski_narx) if variant.eski_narx else None,
                        'stock': variant.soni,
                        'sku': variant.sku,
                        'image': variant.image.url if variant.image else None,
                        'available': variant.mavjud
                    })
                    break

    # Pre-serialize each option group's values to JSON
    variant_options_json = {}
    for key, val in variant_options.items():
        variant_options_json[key] = json.dumps(val['values'])

    default_variant = variantlar.filter(soni__gt=0).first()

    context = {
        'mahsulot': mahsulot,
        'fikrlar': fikrlar,
        'ortacha_reyting': round(ortacha_reyting, 1),
        'bog_liq_mahsulotlar': bog_liq_mahsulotlar,
        'variantlar': variantlar,
        'variant_options': variant_options,
        'variant_options_json': variant_options_json,
        'default_variant': default_variant,
    }
    return render(request, 'mahsulot_detali.html', context)


@require_POST
def variant_info(request, mahsulot_id):
    try:
        data = json.loads(request.body)
        option_ids = data.get('options', [])
        
        variant = MahsulotVariant.objects.filter(
            mahsulot_id=mahsulot_id,
            is_active=True,
            variant_ops__option_value_id__in=option_ids
        ).prefetch_related(
            'variant_ops__option_value__option_type',
            'rasmlar'
        ).distinct().first()
        
        if not variant:
            return JsonResponse({
                'success': False,
                'error': 'Variant topilmadi'
            })
        
        option_values = VariantOption.objects.filter(
            variant=variant
        ).select_related('option_value__option_type')
        
        options_data = {}
        for ov in option_values:
            ot = ov.option_value.option_type
            options_data[ot.kalit] = {
                'name': ot.nom,
                'value': ov.option_value.nom,
                'color_code': ov.option_value.rang_kod
            }
        
        main_image = None
        if variant.image:
            main_image = variant.image.url
        elif variant.rasmlar.filter(asosiy=True).exists():
            main_image = variant.rasmlar.filter(asosiy=True).first().rasm.url
        
        return JsonResponse({
            'success': True,
            'variant': {
                'id': variant.id,
                'price': float(variant.narx),
                'old_price': float(variant.eski_narx) if variant.eski_narx else None,
                'stock': variant.soni,
                'sku': variant.sku,
                'available': variant.mavjud,
                'image': main_image,
                'discount': variant.chegirma_foiz,
            },
            'options': options_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def savatcha(request):
    sessiya_id = request.session.session_key
    if not sessiya_id:
        request.session.create()
        sessiya_id = request.session.session_key

    savatcha_obj, _ = Savatcha.objects.get_or_create(sessiya_id=sessiya_id)

    if request.user.is_authenticated:
        SavatchaMahsulot.objects.filter(savatcha__sessiya_id=sessiya_id).exclude(savatcha__user=request.user).delete()
        if not savatcha_obj.user:
            savatcha_obj.user = request.user
            savatcha_obj.save()

    context = {
        'savatcha': savatcha_obj,
    }
    return render(request, 'savatcha.html', context)


def savatcha_soni_api(request):
    sessiya_id = request.session.session_key
    if not sessiya_id:
        request.session.create()
        sessiya_id = request.session.session_key

    savatcha_obj, _ = Savatcha.objects.get_or_create(sessiya_id=sessiya_id)
    return JsonResponse({'success': True, 'soni': savatcha_obj.soni})


@require_POST
def savatcha_qoshish(request):
    try:
        data = json.loads(request.body)
        mahsulot_id = data.get('mahsulot_id')
        variant_id = data.get('variant_id')
        miqdor = int(data.get('miqdor', 1))

        mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id, is_active=True)
        variant = None
        if variant_id:
            variant = get_object_or_404(MahsulotVariant, id=variant_id)

        sessiya_id = request.session.session_key
        if not sessiya_id:
            request.session.create()
            sessiya_id = request.session.session_key

        savatcha_obj, _ = Savatcha.objects.get_or_create(sessiya_id=sessiya_id)
        if request.user.is_authenticated and not savatcha_obj.user:
            savatcha_obj.user = request.user
            savatcha_obj.save()

        item, created = SavatchaMahsulot.objects.get_or_create(
            savatcha=savatcha_obj,
            mahsulot=mahsulot,
            variant=variant,
            defaults={'miqdor': miqdor}
        )
        if not created:
            item.miqdor += miqdor
            item.save()

        return JsonResponse({'success': True, 'jami': savatcha_obj.jami, 'soni': savatcha_obj.soni})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_POST
def savatcha_miqdor(request, item_id):
    try:
        data = json.loads(request.body)
        miqdor = int(data.get('miqdor', 1))
        item = get_object_or_404(SavatchaMahsulot, id=item_id)
        item.miqdor = max(1, miqdor)
        item.save()
        return JsonResponse({'success': True, 'jami': item.savatcha.jami})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_POST
def savatcha_olib_tashlash(request, item_id):
    try:
        item = get_object_or_404(SavatchaMahsulot, id=item_id)
        savatcha = item.savatcha
        item.delete()
        return JsonResponse({'success': True, 'jami': savatcha.jami, 'soni': savatcha.soni})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_POST
def savatcha_tozalash(request):
    try:
        sessiya_id = request.session.session_key
        if sessiya_id:
            Savatcha.objects.filter(sessiya_id=sessiya_id).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def checkout(request):
    sessiya_id = request.session.session_key
    if not sessiya_id:
        return redirect('savatcha')

    savatcha_obj = get_object_or_404(Savatcha, sessiya_id=sessiya_id)
    if savatcha_obj.mahsulotlar.count() == 0:
        messages.error(request, 'Savatchangiz bo\'sh')
        return redirect('savatcha')

    demo_kartalar = DemoKarta.objects.filter(holat='faol')

    if request.method == 'POST':
        form = BuyurtmaForm(request.POST)
        if form.is_valid():
            buyurtma = Buyurtma.objects.create(
                user=request.user if request.user.is_authenticated else None,
                buyurtma_raqami=str(uuid.uuid4())[:8].upper(),
                ism=form.cleaned_data['ism'],
                familiya=form.cleaned_data['familiya'],
                telefon=form.cleaned_data['telefon'],
                email=form.cleaned_data['email'],
                viloyat=form.cleaned_data['viloyat'],
                raion=form.cleaned_data['raion'],
                manzil=form.cleaned_data['manzil'],
                binolar=form.cleaned_data['binolar'],
                kvartira=form.cleaned_data['kvartira'],
                pochta_kod=form.cleaned_data['pochta_kod'],
                izoh=form.cleaned_data['izoh'],
                tolov_turi=form.cleaned_data['tolov_turi'],
                jami=savatcha_obj.jami,
                ip=request.META.get('REMOTE_ADDR'),
            )

            for item in savatcha_obj.mahsulotlar.all():
                narx = item.variant.narx if item.variant and item.variant.narx else item.mahsulot.narx
                BuyurtmaMahsulot.objects.create(
                    buyurtma=buyurtma,
                    mahsulot=item.mahsulot,
                    variant=item.variant,
                    narx=narx,
                    miqdor=item.miqdor,
                    jami=narx * item.miqdor,
                )
                item.mahsulot.soni = max(0, item.mahsulot.soni - item.miqdor)
                item.mahsulot.sotish_soni += item.miqdor
                item.mahsulot.save(update_fields=['soni', 'sotish_soni'])

            tolov = Tolom.objects.create(
                buyurtma=buyurtma,
                tolov_turi=buyurtma.tolov_turi,
                summa=buyurtma.jami,
            )

            savatcha_obj.mahsulotlar.all().delete()
            messages.success(request, 'Buyurtmangiz muvaffaqiyatli yuborildi! Admin tasdiqlashini kuting.')
            return redirect('buyurtma_detali', id=buyurtma.id)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'ism': request.user.first_name,
                'familiya': request.user.last_name,
                'telefon': request.user.telefon,
                'email': request.user.email,
            }
            asosiy_manzil = request.user.manzillar.filter(asosiy=True).first()
            if asosiy_manzil:
                initial.update({
                    'viloyat': asosiy_manzil.viloyat,
                    'raion': asosiy_manzil.raion,
                    'manzil': asosiy_manzil.manzil,
                    'binolar': asosiy_manzil.binolar,
                    'kvartira': asosiy_manzil.kvartira,
                    'pochta_kod': asosiy_manzil.pochta_kod,
                })
        form = BuyurtmaForm(initial=initial)

    viloyatlar = ViloyatRaioni.objects.filter(is_active=True).values_list('viloyat', flat=True).distinct()

    context = {
        'form': form,
        'savatcha': savatcha_obj,
        'viloyatlar': viloyatlar,
        'demo_kartalar': demo_kartalar,
    }
    return render(request, 'checkout.html', context)


def chek(request, id):
    buyurtma = get_object_or_404(Buyurtma, id=id)
    if request.user.is_authenticated and buyurtma.user != request.user:
        messages.error(request, 'Siz bu buyurtmani ko\'ra olmaysiz')
        return redirect('mening_buyurtmalarim')

    tolov = buyurtma.tolovlar.first()
    demo_karta = tolov.demo_karta if tolov else None

    context = {
        'buyurtma': buyurtma,
        'tolov': tolov,
        'demo_karta': demo_karta,
    }
    return render(request, 'chek.html', context)


def buyurtma_detali(request, id):
    buyurtma = get_object_or_404(Buyurtma, id=id)
    if request.user.is_authenticated and buyurtma.user != request.user:
        messages.error(request, 'Siz bu buyurtmani ko\'ra olmaysiz')
        return redirect('mening_buyurtmalarim')
    tolov = buyurtma.tolovlar.first()
    demo_karta = tolov.demo_karta if tolov else None
    context = {
        'buyurtma': buyurtma,
        'tolov': tolov,
        'demo_karta': demo_karta,
    }
    return render(request, 'buyurtma_detali.html', context)


def mening_buyurtmalarim(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    buyurtmalar = Buyurtma.objects.filter(user=request.user)
    context = {'buyurtmalar': buyurtmalar}
    return render(request, 'mening_buyurtmalarim.html', context)


def kirish(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = KirishForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if form.cleaned_data['eslab_qol']:
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Foydalanuvchi nomi yoki parol noto\'g\'ri')
    else:
        form = KirishForm()

    context = {'form': form}
    return render(request, 'kirish.html', context)


def royxatdan_otish(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RoyxatanOtishForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Ro\'yxatdan muvaffaqiyatli o\'tdingiz!')
            return redirect('index')
    else:
        form = RoyxatanOtishForm()

    context = {'form': form}
    return render(request, 'royxatdan_otish.html', context)


def chiqish(request):
    logout(request)
    messages.success(request, 'Tizimdan chiqdingiz')
    return redirect('index')


@login_required
def profil(request):
    if request.method == 'POST':
        form = FoydalanuvchiProfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil yangilandi')
            return redirect('profil')
    else:
        form = FoydalanuvchiProfilForm(instance=request.user)

    context = {'form': form}
    return render(request, 'profil.html', context)


@login_required
def parol_ozgartirish(request):
    if request.method == 'POST':
        form = ParolOzgartirishForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parolingiz muvaffaqiyatli o\'zgartirildi')
            return redirect('profil')
    else:
        form = ParolOzgartirishForm(request.user)

    context = {'form': form}
    return render(request, 'parol_ozgartirish.html', context)


@login_required
def dashboard(request):
    buyurtmalar = Buyurtma.objects.filter(user=request.user)[:5]
    jami_buyurtma = Buyurtma.objects.filter(user=request.user).count()
    jami_sarflangan = Buyurtma.objects.filter(user=request.user).aggregate(Sum('jami'))['jami__sum'] or 0

    context = {
        'buyurtmalar': buyurtmalar,
        'jami_buyurtma': jami_buyurtma,
        'jami_sarflangan': jami_sarflangan,
    }
    return render(request, 'dashboard.html', context)


@login_required
def manzillar(request):
    manzillar = request.user.manzillar.all()

    if request.method == 'POST':
        if 'delete' in request.POST:
            manzil_id = request.POST.get('delete')
            manzil = get_object_or_404(FoydalanuvchiManzil, id=manzil_id, user=request.user)
            manzil.delete()
            messages.success(request, 'Manzil o\'chirildi')
            return redirect('manzillar')
        else:
            form = ManzilForm(request.POST)
            if form.is_valid():
                manzil = form.save(commit=False)
                manzil.user = request.user
                manzil.save()
                messages.success(request, 'Manzil qo\'shildi')
                return redirect('manzillar')
    else:
        form = ManzilForm()

    context = {
        'manzillar': manzillar,
        'form': form,
    }
    return render(request, 'manzillar.html', context)


@login_required
def istaknafarim(request):
    istaknafarlar = request.user.istaknafarlar.all()
    context = {'istaknafarlar': istaknafarlar}
    return render(request, 'istaknafarim.html', context)


@login_required
def istakga_qoshish(request, mahsulot_id):
    mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id)
    Istaknafar.objects.get_or_create(user=request.user, mahsulot=mahsulot)
    messages.success(request, 'Mahsulot istaklariga qo\'shildi')
    return redirect('istaknafarim')


@login_required
def istakdan_olib_tashlash(request, mahsulot_id):
    mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id)
    Istaknafar.objects.filter(user=request.user, mahsulot=mahsulot).delete()
    messages.success(request, 'Mahsulot istaklaridan olib tashlandi')
    return redirect('istaknafarim')


@login_required
def sozlamalar(request):
    return render(request, 'sozlamalar.html')


@login_required
def qr_kod(request, id):
    buyurtma = get_object_or_404(Buyurtma, id=id)
    if request.user.is_authenticated and buyurtma.user != request.user:
        messages.error(request, 'Siz bu buyurtmani ko\'ra olmaysiz')
        return redirect('mening_buyurtmalarim')

    if not buyurtma.qr_kod:
        buyurtma.generate_qr_code()

    context = {'buyurtma': buyurtma}
    return render(request, 'qr_kod.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_qr_skaner(request):
    return render(request, 'admin_qr_skaner.html')


@require_POST
@user_passes_test(lambda u: u.is_staff)
def admin_qr_tasdiqlash(request):
    try:
        data = json.loads(request.body)
        qr_data = data.get('qr_data')
        
        if not qr_data:
            return JsonResponse({'success': False, 'error': 'QR kod ma\'lumotlari topilmadi'})

        buyurtma_raqami = qr_data.get('buyurtma_raqami')
        if not buyurtma_raqami:
            return JsonResponse({'success': False, 'error': 'Buyurtma raqami topilmadi'})

        buyurtma = get_object_or_404(Buyurtma, buyurtma_raqami=buyurtma_raqami)
        
        if buyurtma.holat in ['yetkazildi', 'bekor_qilindi']:
            return JsonResponse({'success': False, 'error': 'Buyurtma allaqachon yakunlangan'})

        if buyurtma.holat in ['kutilmoqda', 'tasdiqlandi', 'qr_kutilmoqda']:
            buyurtma.holat = 'qr_tasdiqlandi'
            buyurtma.save(update_fields=['holat'])
            
            KaroshaTarixi.objects.create(
                user=buyurtma.user,
                harakat=f'QR kod tasdiqlandi: {buyurtma.buyurtma_raqami}',
                ip=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
            
            return JsonResponse({
                'success': True,
                'buyurtma_raqami': buyurtma.buyurtma_raqami,
                'ism': buyurtma.ism,
                'familiya': buyurtma.familiya,
                'jami': str(buyurtma.jami),
                'holat': buyurtma.get_holat_display(),
                'mahsulotlar': [
                    {
                        'nom': item.mahsulot.nom,
                        'miqdor': item.miqdor,
                        'narx': str(item.narx),
                    }
                    for item in buyurtma.mahsulotlar.all()
                ]
            })
        else:
            return JsonResponse({'success': False, 'error': f'Buyurtma holati: {buyurtma.get_holat_display()}'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def parol_tiklash(request):
    return render(request, 'parol_tiklash.html')


def buyurtmani_kuzatish(request):
    return render(request, 'buyurtmani_kuzatish.html')


@login_required
def kuponlar(request):
    return render(request, 'kuponlar.html')


@login_required
def bonuslar(request):
    return render(request, 'bonuslar.html')


@login_required
def bildirishnomalar(request):
    return render(request, 'bildirishnomalar.html')


def biz_haqimizda(request):
    return render(request, 'biz_haqimizda.html')


def faq(request):
    return render(request, 'faq.html')


def blog(request):
    return render(request, 'blog.html')


def aloqa(request):
    return render(request, 'aloqa.html')


def brendlar(request):
    brendlar = Brend.objects.filter(is_active=True)
    context = {'brendlar': brendlar}
    return render(request, 'brendlar.html', context)


def aksiyalar(request):
    aksiyalar = Aktsiya.objects.filter(is_active=True)
    context = {'aksiyalar': aksiyalar}
    return render(request, 'aksiyalar.html', context)


def yangi_mahsulotlar(request):
    mahsulotlar = Mahsulot.objects.filter(yangi=True, is_active=True)
    context = {'mahsulotlar': mahsulotlar}
    return render(request, 'yangi_mahsulotlar.html', context)


def ko_p_sotilganlar(request):
    mahsulotlar = Mahsulot.objects.filter(is_active=True).order_by('-sotish_soni')
    context = {'mahsulotlar': mahsulotlar}
    return render(request, 'ko_p_sotilganlar.html', context)


def taqqoslash(request):
    return render(request, 'taqqoslash.html')


def oxirgi_korilgan(request):
    return render(request, 'oxirgi_korilgan.html')


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
