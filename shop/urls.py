from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('', views.index, name='index'),
]
