from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("Добро пожаловать на сайт доставки цветов!")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # главная страница
]
