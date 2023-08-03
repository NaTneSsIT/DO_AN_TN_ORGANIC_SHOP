from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('filter-data', views.filter_data, name='filter_data'),
    path('categories-list', views.categories_list, name='categories-list'),
    path('brands-list', views.brands_list, name='brands-list'),
    path('products-list', views.products_list, name='products-list'),
    path('categories-products-list/<int:cate_id>', views.category_product_list, name='categories-product-list'),
    path('brands-products-list/<int:brand_id>', views.brand_product_list, name='brands-product-list'),
    path('product/<str:slug>/<int:id>', views.product_detail, name='product_detail'),
    path('load-more-data', views.load_more_data, name='load_more_data'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart_list,name='cart'),
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    path('accounts/signup',views.signup,name='signup'),
    path('checkout',views.checkout,name='checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('save-review/<int:pid>', views.save_review, name='save-review'),
]
