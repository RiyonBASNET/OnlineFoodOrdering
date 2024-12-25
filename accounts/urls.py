from django.urls import path
from .views import *

urlpatterns = [
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('success/', success_request, name='success'),
    path('token/', token_send, name='token'),
    path('verify/<auth_token>', verify, name='verify'),
    path('error/', error_page, name='error_page'),
    path('forgetpassword/', forget_password, name='forget_password'),
    path('changepassword/<token>', change_password, name='change_password'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]
