from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

class Banner(models.Model):
    img = models.CharField(max_length=255)
    alt_text = models.CharField(max_length=300)
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="cat_imgs/")

    def image_tag(self):
        return mark_safe(f'<img src={self.image.url} width="50px" height="50px" />')
    def __str__(self):
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="brand_imgs/")

    def image_tag(self):
        return mark_safe(f'<img src={self.image.url} width="50px" height="50px" />')

    def __str__(self):
        return self.brand_name


class Size(models.Model):
    size_name = models.CharField(max_length=255)

    def __str__(self):
        return self.size_name


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="product_imgs/")
    slug = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    is_special = models.BooleanField(default=False)

    def image_tag(self):
        return mark_safe(f'<img src={self.image.url} width="50px" height="50px" />')
    def __str__(self):
        return self.product_name


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    qty = models.IntegerField()

    def __str__(self):
        return self.product.product_name
status_choice=(
        ('Waiting Payment','waiting'),
        ('Ready to ship','ready'),
        ('Shipped','shipped'),
        ('Complete','complete'),
        ('Cancel','cancel'),)
class CartOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amt=models.FloatField()
    paid_status=models.BooleanField(default=False)
    order_dt=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(choices=status_choice,default='Waiting Payment',max_length=150)
    qty = models.IntegerField(null=True)
    qty_remaining = models.IntegerField(null=True)
    class Meta:
        verbose_name_plural='Orders'

class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=150)
    item=models.CharField(max_length=150)
    image=models.CharField(max_length=200)
    qty=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()

    class Meta:
        verbose_name_plural='Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))


RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural='Reviews'

    def get_review_rating(self):
        return self.review_rating

# WishList
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Wishlist'

# AddressBook
class UserAddressBook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=50,null=True)
    address=models.TextField()
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='AddressBook'
