from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name


class FoodItems(models.Model):
    item_name = models.CharField(max_length=50)
    item_price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)
    item_image = models.FileField(upload_to='static/uploads', null=True)
    item_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.item_name
