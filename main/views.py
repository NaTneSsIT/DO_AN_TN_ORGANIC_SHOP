from django.shortcuts import render
from .models import Category, Brand, Product, Size

# Create your views here.
def home(request):
    return render(request, 'index.html')


def categories_list(request):
    data = Category.objects.all()
    return render(request, 'categories.html', {"data": data})

def brands_list(request):
    data = Brand.objects.all()
    return render(request, 'brands.html', {"data": data})

def products_list(request):
    pro_data = Product.objects.all()
    cate_data = Category.objects.distinct().values()
    brand_data = Brand.objects.distinct().values()
    size_data = Size.objects.distinct().values()
    return render(request, 'products.html', {"data": pro_data, "cate_data": cate_data,"brand_data":brand_data,"size_data":size_data})