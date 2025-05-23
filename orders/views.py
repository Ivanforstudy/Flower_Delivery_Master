from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm
from .models import Order
from catalog.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            order.products.add(product)
            return redirect('orders:order_success')
    else:
        form = OrderForm()
    return render(request, 'orders/create_order.html', {'form': form, 'product': product})

@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})
