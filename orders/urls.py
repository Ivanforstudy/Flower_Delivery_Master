from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('history/', views.order_history, name='order_history'),
    path('create/<int:product_id>/', views.create_order, name='create_order'),
]
