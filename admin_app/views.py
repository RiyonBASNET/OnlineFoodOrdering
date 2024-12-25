from django.contrib.auth.decorators import login_required
from accounts.auth import admin_only
from multiprocessing import context
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .forms import *
import os
from admin_app.models import FoodItems
from django.contrib import messages
from userspage.models import Order
from django.contrib.auth.models import User

# Create your views here.


@login_required
@admin_only
def show_items(request):
    items = FoodItems.objects.all().order_by('-id')
    context = {
        'items': items
    }
    return render(request, 'demo/index.html', context)


@login_required
@admin_only
def post_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Category added successfully')
            return redirect('/admin/addcategory')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Unable to add category')
            return render(request, 'demo/addcategory.html', {'form': form})

    context = {
        'form': CategoryForm
    }
    return render(request, 'demo/addcategory.html', context)


@login_required
@admin_only
def post_items(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Item Added Successfully')
            return redirect('/admin/additem')
        else:
            messages.add_message(request, messages.ERROR, 'Unale to Add Item')
            return render(request, 'demo/additem.html', {'form': form})

    context = {
        'form': ItemForm
    }
    return render(request, 'demo/additem.html', context)


@login_required
@admin_only
def show_category(request):
    category = Category.objects.all()
    context = {
        'category': category
    }
    return render(request, 'demo/category.html', context)


@login_required
@admin_only
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, 'Category Deleted')
    return redirect('/admin/category')


@login_required
@admin_only
def update_category_form(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category Updated')
            return redirect('/admin/category')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Unable to Update Category')
            return render(request, 'demo/updatecategory.html', {'form': form})
    context = {
        'form': CategoryForm(instance=category)
    }
    return render(request, 'demo/updatecategory.html', context)


@login_required
@admin_only
def delete_item(request, item_id):
    item = FoodItems.objects.get(id=item_id)
    os.remove(item.item_image.path)
    item.delete()
    messages.add_message(request, messages.SUCCESS,
                         'Item Deleted Successfully')
    return redirect('/admin/product')


@login_required
@admin_only
def update_item_form(request, item_id):
    item = FoodItems.objects.get(id=item_id)
    if request.method == 'POST':
        if request.FILES.get('item_image'):
            os.remove(item.item_image.path)
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Item Updated Successfully')
            return redirect('/admin/product')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Unable to Update Item')
            return render(request, 'demo/updateitem.html', {'form': form})
    context = {
        'form': ItemForm(instance=item)
    }
    return render(request, 'demo/updateitem.html', context)


@login_required
@admin_only
def user_order(request):
    items = Order.objects.all()
    context = {
        'items': items
    }
    return render(request, 'demo/userorder.html', context)


@login_required
@admin_only
def users(request):
    user = User.objects.all()
    context = {
        'users': user
    }
    return render(request, 'demo/dashboard.html', context)
