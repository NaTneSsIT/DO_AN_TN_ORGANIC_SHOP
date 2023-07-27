from django.db import models
from django.utils.safestring import mark_safe


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
    specs = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.product.product_name
