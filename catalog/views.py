from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import CombinedProductVersionForm, ContactForm
from catalog.models import Product, Version


# Create your views here.

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = CombinedProductVersionForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        """Привязка пользователя к продукту"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['object_list']:
            product_versions = Version.objects.filter(product=product)
            current_version = product_versions.filter(is_current_version=True).first()
            product.current_version = current_version
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = CombinedProductVersionForm
    success_url = reverse_lazy('catalog:product_list')


class ProductDetailView(DetailView):
    model = Product


class ProductDeleteView(LoginRequiredMixin, DeleteView):
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
