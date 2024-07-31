from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import ProductListView, ProductDetailView, ContactView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, CategoryListView

app_name = 'catalog'

urlpatterns = [
    path('', cache_page(60)(ProductListView.as_view()), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_form'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product_detail/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
]
