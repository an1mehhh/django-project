from django.shortcuts import render

from catalog.models import Product, Category


# Create your views here.

def index(request):
    context = {
        'category': Category.objects.all()
    }
    return render(request, 'catalog/index.html', context)


def product_list(request):
    products = Product.objects.all()  # Получаем все продукты
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)  # Получаем продукт по его pk
    return render(request, 'catalog/product_detail.html', {'product': product})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name} \nТелефон: {phone} \nСообщение: {message}')

    return render(request, 'catalog/contacts.html')
