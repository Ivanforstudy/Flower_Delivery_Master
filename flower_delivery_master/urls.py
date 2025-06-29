from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),       # ← это обязательно!
    path('catalog/', include('catalog.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('accounts.urls')),
    path('reviews/', include('reviews.urls')),
    path('analytics/', include('analytics.urls')),
    path('telegram/', include('telegram_bot.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
