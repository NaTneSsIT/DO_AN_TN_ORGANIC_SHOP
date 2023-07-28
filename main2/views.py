from django.shortcuts import render
from .models import Category, Brand, Product, Size


# Create your views here.
def home(request):
    pro_data = Product.objects.filter(is_special=True)
    return render(request, 'index.html', {"data": pro_data})


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
    return render(request, 'products.html',
                  {"data": pro_data, "cate_data": cate_data, "brand_data": brand_data, "size_data": size_data})


def category_product_list(request, cate_id):
    cate = Category.objects.get(id=cate_id)
    data = Product.objects.filter(category=cate)
    return render(request, 'category_product_list.html', {"data": data, "cate": cate})

def brand_product_list(request, brand_id):
    bra = Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=bra)
    return render(request, 'brand_product_list.html', {"data": data, "bra": bra})
