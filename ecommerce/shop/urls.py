
from django.contrib import admin
from django.urls import path

from shop import views

app_name='shop'
urlpatterns = [
    path('',views.home,name='home'),
    path('category',views.category,name='category'),
    path('product/<int:i>',views.product,name='product'),
    path('productdetails/<int:i>',views.productdetails,name='productdetails'),
    path('register',views.register,name='register'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout')

]
