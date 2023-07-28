from django.shortcuts import render
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
