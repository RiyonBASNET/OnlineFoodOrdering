from django.contrib.auth.models import User
import profile
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from email import message
from unicodedata import category
import requests as req
from django.shortcuts import render, redirect
from accounts.models import Profile
from admin_app.models import *
from django.contrib.auth.decorators import login_required
from accounts.auth import user_only
from userspage.forms import OrderForm
from userspage.models import Order, OrderList
from django.contrib import messages
from .filters import ItemFilter


def homepage(request):
    items = FoodItems.objects.all().order_by('-id')[:8]
    all_items = FoodItems.objects.all()[:8]
    context = {
        'items': items,
        'all_items': all_items
    }
    return render(request, 'client/homepage.html', context)


def itemspage(request):
    items = FoodItems.objects.all()
    burgers = items.filter(item_name__icontains='burger').values()
    sandwich = items.filter(item_description__icontains='sandwich').values()
    snacks = items.filter(item_description__icontains='snack').values()
    pizza = items.filter(item_description__icontains='pizza').values()
    momo = items.filter(item_description__icontains='momo').values()
    item_filter = ItemFilter(request.GET, queryset=items)
    item_final = item_filter.qs

    context = {
        'items': item_final,
        'item_filter': item_filter,
        'burger': burgers,
        'sandwich': sandwich,
        'snacks': snacks,
        'pizza': pizza,
        'momo': momo
    }
    return render(request, 'client/itempage.html', context)


def item_details(request, item_id):
    items = FoodItems.objects.get(id=item_id)
    context = {
        'items': items
    }
    return render(request, 'client/itemdetails.html', context)


def blog(request):
    return render(request, 'client/blog.html')


def faqs(request):
    return render(request, 'client/faqpage.html')


def about(request):
    return render(request, 'client/aboutpage.html')


@login_required
@user_only
def add_order(request, item_id):
    user = request.user
    items = FoodItems.objects.get(id=item_id)

    check_items_presence = OrderList.objects.filter(user=user, items=items)
    if check_items_presence:
        messages.add_message(request, messages.ERROR,
                             'Item already in the list')
        return redirect('/myorderlist')
    else:
        orderlist = OrderList.objects.create(items=items, user=user)
        if orderlist:
            messages.add_message(request, messages.SUCCESS,
                                 'Item added to List')
            return redirect('/myorderlist')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Unable to add item in List')
            return redirect('/menu')


@login_required
@user_only
def show_orderlist(request):
    user = request.user
    items = OrderList.objects.filter(user=user).order_by('-id')
    context = {
        'items': items
    }
    return render(request, 'client/orderlist.html', context)


@login_required
@user_only
def order_form(request, item_id, orderlist_id):
    user = request.user

    # profile = Profile.objects.all()

    # user_obj = User.objects.filter()
    # email=
    item = FoodItems.objects.get(id=item_id)
    list_item = OrderList.objects.get(id=orderlist_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            quantity = request.POST.get('quantity')

            # email = request.POST.get('email')

            if int(quantity) <= 0:
                messages.error(request, 'Cannot be 0 or negative')
                return render(request, 'client/orderform.html', {'form': form})
            price = item.item_price
            total_price = int(quantity)*int(price)
            contact_no = request.POST.get('contact_no')
            address = request.POST.get('address')
            payment_method = request.POST.get('payment_method')
            payment_status = request.POST.get('payment_status')
            status = request.POST.get('status')

            order = Order.objects.create(
                items=item,
                user=user,
                quantity=quantity,
                total_price=total_price,
                contact_no=contact_no,
                address=address,
                payment_method=payment_method,
                payment_status=payment_status,
                status=status,
            )
            if order.payment_method == 'Cash on Delivery':
                list_item = OrderList.objects.get(id=orderlist_id)
                list_item.delete()
                messages.add_message(
                    request, messages.SUCCESS, 'Order Successful')

                # order_placed(user, email)
                # print(email)

                return redirect('/myorderlist')
            elif order.payment_method == 'eSewa':
                context = {
                    'order': order,
                    'list_item': list_item
                }
                return render(request, 'client/esewapayment.html', context)
            else:
                messages.add_message(
                    request, messages.ERROR, 'Something went wrong')
                return render(request, 'client/orderform.html', {'form': form})
    context = {
        'form': OrderForm,
        # 'profile': profile,
    }
    return render(request, 'client/orderform.html', context)


def order_placed(user, email):
    subject = "Order Placed"
    message = f"Hello {user}. Your order has been placed."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


@login_required
@user_only
def show_orders(request):
    user = request.user
    items = Order.objects.filter(user=user)
    context = {
        'items': items
    }
    return render(request, 'client/order.html', context)


def esewa_verify(request):
    import xml.etree.ElementTree as ET

    o_id = request.GET.get('oid')
    amount = request.GET.get('amt')
    refId = request.GET.get('refId')

    url = "https://uat.esewa.com.np/epay/main"
    d = {
        'amt': amount,
        'scd': 'EPAYTEST',
        'rid': refId,
        'pid': o_id,
    }
    resp = req.post(url, d)
    root = ET.fromstring(resp.content)
    status = root[0].text.strip()
    if status == 'Success':
        order_id = o_id.split("_")[0]
        order = Order.objects.get(id=order_id)
        order.payment_status = True
        order.save()
        orderlist_id = o_id.split("_")[1]
        orderlist = OrderList.objects.get(id=orderlist_id)
        orderlist.delete()
        messages.add_message(request, messages.SUCCESS, 'payment Successfull')
        return redirect('/myorders')
    else:
        messages.add_message(request, messages.ERROR, 'Unable to make Payment')
        return redirect('/myorders')


@login_required
@user_only
def remove_order_item(request, orderlist_id):
    item = OrderList.objects.get(id=orderlist_id)
    item.delete()
    messages.add_message(request, messages.SUCCESS,
                         'Item removed Successfully')
    return redirect('/myorderlist')


@login_required
@user_only
def change_user_password(request, username):
    if request.method == 'POST':
        u = User.objects.get(username=username)

        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Password did not match')
            return redirect(f'/changepassword/{username}')
        u.set_password(new_password)
        u.save()

        user = authenticate(request, username=username, password=new_password)
        login(request, user)
        return redirect('/')

    return render(request, 'client/change_password.html')
