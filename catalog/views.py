from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import CombinedProductVersionForm, ContactForm, ProductModeratorForm
from catalog.models import Product, Version, Category
from catalog.services import get_cached_categories, get_cached_products


# Create your views here.

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return get_cached_categories()


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return get_cached_products()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['products']:
            product_versions = Version.objects.filter(product=product)
            current_version = product_versions.filter(is_current_version=True).first()
            product.current_version = current_version
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = CombinedProductVersionForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        """Привязка пользователя к продукту"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    model = Product
    form_class = CombinedProductVersionForm
    permission_required = 'catalog.change_product'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            product = form.save(commit=False)  # Сохраняем форму без коммита
            user = self.request.user
            product.owner = user
            product.save()  # Сохраняем продукт с установленным владельцем
            formset.instance = product
            formset.save()  # Сохраняем формсет
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return CombinedProductVersionForm
        elif user.has_perms(
                ["catalog.cancel_publication", "catalog.can_edit_description", "catalog.can_edit_category", ]):
            return ProductModeratorForm
        else:
            raise PermissionDenied


class ProductDetailView(LoginRequiredMixin, DetailView):
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
