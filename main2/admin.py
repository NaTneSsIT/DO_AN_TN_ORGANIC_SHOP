from django.contrib import admin
from .models import Category, Brand, Size, Product, ProductAttribute, Banner

# Register your models here.


admin.site.register(Size)
admin.site.register(Banner)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', "image_tag")


admin.site.register(Brand, BrandAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', "image_tag")


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', "product_name", "sku", 'brand', "status", "is_special")
    list_editable = ('status', 'is_special')


admin.site.register(Product, ProductAdmin)


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', "product", "price", "size")


admin.site.register(ProductAttribute, ProductAttributeAdmin)
