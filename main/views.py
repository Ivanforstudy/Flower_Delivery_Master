from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')

def logout_success(request):
    return render(request, 'main/logout_success.html')
