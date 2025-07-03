from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm


def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})


def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews:review_list')
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form})
