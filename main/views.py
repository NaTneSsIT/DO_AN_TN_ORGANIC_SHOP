from django.shortcuts import render
from .models import Category, Brand

# Create your views here.
def home(request):
    return render(request, 'index.html')


def categories_list(request):
    data = Category.objects.all()
    return render(request, 'categories.html', {"data": data})

def brands_list(request):
    data = Brand.objects.all()
    return render(request, 'brands.html', {"data": data})