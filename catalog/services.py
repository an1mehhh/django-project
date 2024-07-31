from django.core.cache import cache

from catalog.models import Category, Product


def get_cached_categories():
    categories = cache.get('categories_list')
    if categories is None:
        categories = list(Category.objects.all())

    return categories


def get_cached_products():
    products = cache.get('products_list')
    if products is None:
        products = list(Product.objects.filter(is_published=True))

    return products

