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
    path('my-dashboard', views.my_dashboard, name='my_dashboard'),
    path('my-orders', views.my_orders, name='my_orders'),
    path('my-orders-items/<int:id>', views.my_order_items, name='my_order_items'),
    path('add-wishlist', views.add_wishlist, name='add_wishlist'),
    path('my-wishlist', views.my_wishlist, name='my_wishlist'),
    path('my-reviews', views.my_reviews, name='my-reviews'),
    path('my-addressbook', views.my_addressbook, name='my-addressbook'),
    path('add-address', views.save_address, name='add-address'),
    path('activate-address', views.activate_address, name='activate-address'),
    path('update-address/<int:id>', views.update_address, name='update-address'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
]
