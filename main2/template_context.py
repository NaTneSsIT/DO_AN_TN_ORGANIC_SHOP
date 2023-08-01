from .models import Product, ProductAttribute
from django.db.models import Min, Max


def get_filters(request):
    cats = Product.objects.distinct().values('category__category_name', 'category__id')
    brands = Product.objects.distinct().values('brand__brand_name', 'brand__id')
    sizes = ProductAttribute.objects.distinct().values('size__size_name', 'size__id')
    minMaxPrice = ProductAttribute.objects.aggregate(Min('price'), Max('price'))
    data = {
        'cats': cats,
        'brands': brands,
        'sizes': sizes,
        'minMaxPrice': minMaxPrice,
    }
    return data
