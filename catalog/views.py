from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ContactForm
from catalog.models import Product


# Create your views here.

class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price',)
    success_url = reverse_lazy('catalog:product_list')


class ProductListView(ListView):
    model = Product


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price',)
    success_url = reverse_lazy('catalog:product_list')


class ProductDetailView(DetailView):
    model = Product


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')


class ContactView(View):
    form_class = ContactForm
    initial = {'key': 'value'}
    template_name = 'catalog/contacts.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print(
                f"Имя: {form.cleaned_data['name']} \nТелефон: {form.cleaned_data['phone']} \nСообщение: {form.cleaned_data['message']}")
            return HttpResponse('Сообщение отправлено!')
        return render(request, self.template_name, {'form': form})
