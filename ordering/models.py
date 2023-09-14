from django.db import models
from myaccount.models import Profile, User
from product.models import Product

class Status(models.Model):
    name = models.CharField(max_length=20)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, default='1', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    company_name = models.CharField(max_length=100)
    delivery_date = models.DateField()

    def __str__(self):
        return f"Заказ #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price