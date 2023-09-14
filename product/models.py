from django.contrib.sessions.models import Session
from django.db import models
from myaccount.models import Profile
from django.contrib.auth.models import User



def product_main_image(instance, filename):
    return 'products/product_{pk}/main_image/{filename}'.format(pk=instance.pk, filename=filename)

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weight = models.CharField(default='шт.', max_length=20)
    main_image = models.ImageField(upload_to=product_main_image)
    archived = models.BooleanField(default=True)


    def __str__(self):
        return self.name

def product_images(instance, filename):
    return 'products/product_{pk}/images/{filename}'.format(pk=instance.product.pk, filename=filename)
class ProductImage(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(null = True, blank=True, upload_to=product_images)


