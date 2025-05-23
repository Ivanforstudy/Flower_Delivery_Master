from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from .forms import ReviewForm
from catalog.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('catalog:product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form, 'product': product})
