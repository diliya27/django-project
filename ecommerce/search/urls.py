
from django.contrib import admin
from django.urls import path
from search import views
app_name='search'
urlpatterns = [
    path('search_product/',views.search_product,name='search_product'),
]
