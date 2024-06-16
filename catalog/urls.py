from django.urls import path

from catalog.views import index, contact

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contact, name='contacts'),
]