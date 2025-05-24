from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("Добро пожаловать в Flower Delivery Master!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # добавь это
]
