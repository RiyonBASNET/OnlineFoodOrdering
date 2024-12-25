from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.show_items),
    path('addcategory/', views.post_category),
    path('additem/', views.post_items),
    path('category/', views.show_category),
    path('deletecategory/<int:category_id>', views.delete_category),
    path('updatecategory/<int:category_id>', views.update_category_form),
    path('deleteitem/<int:item_id>', views.delete_item),
    path('updateitem/<int:item_id>', views.update_item_form),
    path('usersorder/', views.user_order),
    path('dashboard/', views.users),
]
