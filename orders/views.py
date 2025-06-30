from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalog.models import Product
from .models import Order

@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order = Order.objects.create(user=request.user)
    order.products.add(product)
    order.save()
    return redirect('orders:order_history')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})
