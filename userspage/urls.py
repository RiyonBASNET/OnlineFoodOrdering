
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('menu/', views.itemspage),
    path('itemdetails/<int:item_id>', views.item_details),
    path('add_order/<int:item_id>', views.add_order),
    path('myorderlist/', views.show_orderlist),
    path('orderform/<int:item_id>/<int:orderlist_id>', views.order_form),
    path('myorders/', views.show_orders),
    path('esewa_verify/', views.esewa_verify),
    path('remove_item/<int:orderlist_id>', views.remove_order_item),
    path('faqs/', views.faqs),
    path('blog/', views.blog),
    path('about/', views.about),
    path('change_user_password/<str:username>', views.change_user_password,
         name='change_user_password'),
]
