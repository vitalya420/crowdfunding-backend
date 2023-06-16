from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class OrderLine(models.Model):
    good = models.ForeignKey('store.Goods', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.good.name} - Amount: {self.amount}"


class Goods(models.Model):
    image = models.ImageField(upload_to=upload_to, null=True, default=None)
    name = models.CharField(max_length=128, default=None, null=True)
    description = models.TextField(default=None, null=True)
    price = models.FloatField(default=None, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_lines = models.ManyToManyField(OrderLine)

    def calculate_total_price(self):
        total_price = 0
        for order_line in self.order_lines.all():
            total_price += order_line.good.price * order_line.amount
        return total_price


class DestinationAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=32)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_lines = models.ManyToManyField(OrderLine)
    address = models.ForeignKey(DestinationAddress, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
