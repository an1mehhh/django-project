from django.urls import path

from client.apps import ClientConfig
from client.views import ClientCreateView, ClientListView, ClientDetailView, ClientDeleteView

app_name = ClientConfig.name

urlpatterns = [
    path('create-client/', ClientCreateView.as_view(), name='create-client'),
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('client-detail/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('client-delete/<int:pk>/', ClientDeleteView.as_view(), name='client-delete'),
]
