from django.contrib import admin
from .models import Cart
from .models import Order_table,Payment
# Register your models here.
admin.site.register(Cart)
admin.site.register(Order_table)
admin.site.register(Payment)