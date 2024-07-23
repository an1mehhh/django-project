from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from client.forms import ClientForm
from client.models import Client


# Create your views here.

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'
    success_url = reverse_lazy('users:profile')


class ClientListView(ListView):
    model = Client
    template_name = 'client/client_list.html'
    context_object_name = 'clients'


class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('client:client-list')
