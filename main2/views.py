from django.db.models import Min, Max
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .models import Category, Brand, Product, Size, ProductAttribute


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
    total_data = Product.objects.count()
    data = Product.objects.all().order_by('-id')[:3]
    cate_data = Category.objects.distinct().values()
    brand_data = Brand.objects.distinct().values()
    size_data = Size.objects.distinct().values()
    min_price = ProductAttribute.objects.aggregate(Min('price'))
    max_price = ProductAttribute.objects.aggregate(Max('price'))
    return render(request, 'products.html',
                  {"data": data,
                   'total_data': total_data,
                   "min_price": min_price,
                   "max_price": max_price})


def category_product_list(request, cate_id):
    cate = Category.objects.get(id=cate_id)
    data = Product.objects.filter(category=cate)
    return render(request, 'category_product_list.html', {"data": data, "cate": cate})


def brand_product_list(request, brand_id):
    bra = Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=bra)
    return render(request, 'brand_product_list.html', {"data": data, "bra": bra})


def product_detail(request, slug, id):
    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    sizes = ProductAttribute.objects.filter(product=product).values('size_id', 'size__size_name', 'price').distinct()
    # reviewForm = ReviewAdd()
    #
    # # Check
    # canAdd = True
    # reviewCheck = ProductReview.objects.filter(user=request.user, product=product).count()
    # if request.user.is_authenticated:
    #     if reviewCheck > 0:
    #         canAdd = False
    # # End
    #
    # # Fetch reviews
    # reviews = ProductReview.objects.filter(product=product)
    # # End
    #
    # # Fetch avg rating for reviews
    # avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    # # End

    return render(request, 'product_detail.html',
                  {'data': product, 'related': related_products, 'sizes': sizes})


def search(request):
    q = request.GET['q']
    data = Product.objects.filter(product_name__icontains=q).order_by('-id')
    return render(request, 'search.html', {'data': data})


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts = allProducts.filter(productattribute__price__gte=minPrice)
    allProducts = allProducts.filter(productattribute__price__lte=maxPrice)
    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()
    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(productattribute__size__id__in=sizes).distinct()
    t = render_to_string('ajax/product-list.html', {'data': allProducts})
    return JsonResponse({'data': t})


def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Product.objects.all().order_by('-id')[offset:offset + limit]
    t = render_to_string('ajax/product-list.html', {'data': data})
    return JsonResponse({'data': t}
                        )
