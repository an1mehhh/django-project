from django.urls import path

from catalog.views import index, contact, product_list, product_detail

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contact, name='contacts'),
    path('product_list/', product_list, name='product_list'),
    path('product_detail/<int:pk>/', product_detail, name='product_detail'),
]
