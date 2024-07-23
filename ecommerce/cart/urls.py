
from django.contrib import admin
from django.urls import path
from cart import views
app_name='cart'
urlpatterns = [
    path('add_to_cart/<int:pk>',views.add_to_cart,name='add_to_cart'),
    path('cart_view/',views.cart_view,name='cart_view'),
    path('cart_decrement/<int:d>', views.cart_decrement, name='cart_decrement'),
    path('cart_trash/<int:p>',views.cart_trash,name='cart_trash'),
    path('place_order',views.orderform,name='place_order'),
    path('status/<u>',views.payment_status,name='payment_sataus'),
    path('order_view',views.order_view,name='order_view')

]
