from django.contrib import admin
from .models import Category, Brand, Size, Product, ProductAttribute, Banner, ProductReview, CartOrder, CartOrderItems, \
    Wishlist, UserAddressBook

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
    list_display = ('id', "product_name", "image_tag", "sku", 'brand', "status", "is_special")
    list_editable = ('status', 'is_special')


admin.site.register(Product, ProductAdmin)


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', "product", "price", "size", "qty")


admin.site.register(ProductAttribute, ProductAttributeAdmin)


class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ('paid_status', 'order_status')
    list_display = ('user', 'total_amt', 'paid_status', 'order_dt', 'order_status')


admin.site.register(CartOrder, CartOrderAdmin)


class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'item', 'image_tag', 'qty', 'price', 'total')


admin.site.register(CartOrderItems, CartOrderItemsAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'review_text', 'get_review_rating')


admin.site.register(ProductReview, ProductReviewAdmin)

admin.site.register(Wishlist)


class UserAddressBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'status')


admin.site.register(UserAddressBook, UserAddressBookAdmin)
