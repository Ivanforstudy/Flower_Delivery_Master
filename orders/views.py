from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from catalog.models import Product


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def create_order(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('products')
        if not product_ids:
            return redirect('catalog:product_list')
        order = Order.objects.create(user=request.user)
        products = Product.objects.filter(id__in=product_ids)
        order.products.set(products)
        order.save()
        return redirect('orders:order_detail', pk=order.pk)

    products = Product.objects.all()
    return render(request, 'orders/create_order.html', {'products': products})
