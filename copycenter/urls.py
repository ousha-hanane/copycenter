from django.contrib import admin
from django.urls import path, include
from core.views import home  # 👈 on importe la vue home

# 👇 import nécessaire pour servir les fichiers media en dev
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home"),  # 👈 page d’accueil
    path("admin/", admin.site.urls),
    path("orders/", include("orders.urls")),   # tes commandes
    path("accounts/", include("django.contrib.auth.urls")),  # ✅ login/logout
    path("accounts/", include("accounts.urls")),  # ✅ inscription
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
