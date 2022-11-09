from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'shop/index.html')


def category_products(request, slug):
    return redirect('shop:index')