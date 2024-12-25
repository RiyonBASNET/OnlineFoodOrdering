from django.forms import ModelForm, fields

from userspage.models import Order

from .models import *


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ItemForm(ModelForm):
    class Meta:
        model = FoodItems
        fields = '__all__'
