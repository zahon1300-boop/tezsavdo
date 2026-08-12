from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Backward-compatible /uz/ redirects
uz_redirects = [
    path('uz/', RedirectView.as_view(url='/', permanent=True)),
    path('uz/mahsulotlar/', RedirectView.as_view(url='/mahsulotlar/', permanent=True)),
    path('uz/savatcha/', RedirectView.as_view(url='/savatcha/', permanent=True)),
    path('uz/aksiyalar/', RedirectView.as_view(url='/aksiyalar/', permanent=True)),
    path('uz/biz-haqimizda/', RedirectView.as_view(url='/biz-haqimizda/', permanent=True)),
    path('uz/faq/', RedirectView.as_view(url='/faq/', permanent=True)),
    path('uz/blog/', RedirectView.as_view(url='/blog/', permanent=True)),
    path('uz/aloqa/', RedirectView.as_view(url='/aloqa/', permanent=True)),
    path('uz/brendlar/', RedirectView.as_view(url='/brendlar/', permanent=True)),
    path('uz/yangi-mahsulotlar/', RedirectView.as_view(url='/yangi-mahsulotlar/', permanent=True)),
    path('uz/ko-p-sotilganlar/', RedirectView.as_view(url='/ko-p-sotilganlar/', permanent=True)),
    path('uz/taqqoslash/', RedirectView.as_view(url='/taqqoslash/', permanent=True)),
    path('uz/oxirgi-korilgan/', RedirectView.as_view(url='/oxirgi-korilgan/', permanent=True)),
    path('uz/kirish/', RedirectView.as_view(url='/kirish/', permanent=True)),
    path('uz/royxatdan-otish/', RedirectView.as_view(url='/royxatdan-otish/', permanent=True)),
    path('uz/profil/', RedirectView.as_view(url='/profil/', permanent=True)),
    path('uz/dashboard/', RedirectView.as_view(url='/dashboard/', permanent=True)),
    path('uz/mening-buyurtmalarim/', RedirectView.as_view(url='/mening-buyurtmalarim/', permanent=True)),
    path('uz/manzillarni-boshqarish/', RedirectView.as_view(url='/manzillarni-boshqarish/', permanent=True)),
    path('uz/istaknafarim/', RedirectView.as_view(url='/istaknafarim/', permanent=True)),
    path('uz/sozlamalar/', RedirectView.as_view(url='/sozlamalar/', permanent=True)),
    path('uz/kuponlar/', RedirectView.as_view(url='/kuponlar/', permanent=True)),
    path('uz/bonuslar/', RedirectView.as_view(url='/bonuslar/', permanent=True)),
    path('uz/bildirishnomalar/', RedirectView.as_view(url='/bildirishnomalar/', permanent=True)),
    path('uz/checkout/', RedirectView.as_view(url='/checkout/', permanent=True)),
    path('uz/api/savatcha/qoshish/', RedirectView.as_view(url='/api/savatcha/qoshish/', permanent=True)),
    path('uz/api/mahsulot/<int:mahsulot_id>/variant/', RedirectView.as_view(url='/api/mahsulot/%(mahsulot_id)s/variant/', permanent=True)),
]

urlpatterns += uz_redirects
urlpatterns += [
    path('', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
