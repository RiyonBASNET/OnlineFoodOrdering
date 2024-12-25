from wsgiref import validate
from django.db import models

from admin_app.models import *
from django.contrib.auth.models import User
# Create your models here.


class OrderList(models.Model):
    items = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    PAYMENT = (
        ('Cash on Delivery', 'Cash on Delivery'),
        ('eSewa', 'eSewa'),
    )
    items = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.IntegerField(null=True)
    status = models.CharField(default='Pending', max_length=200, null=True)
    payment_method = models.CharField(max_length=200, choices=PAYMENT)
    payment_status = models.BooleanField(default=False, null=True)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=80)
    order_date = models.DateTimeField(auto_now_add=True)
