import json
import os


from django.conf import settings
from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        path_category = os.path.join(settings.BASE_DIR, 'fixtures/catalog_category_data.json')
        with open(path_category, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            return json_data

    @staticmethod
    def json_read_products():
        path_product = os.path.join(settings.BASE_DIR, 'fixtures/catalog_product_data.json')
        with open(path_product, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            return json_data

    def handle(self, *args, **options):

        # Удалите все продукты
        # Удалите все категории
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(**category['fields'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            try:
                # Получение категории из базы данных для корректной связки объектов
                category = Category.objects.get(pk=product['fields']['category'])
                product['fields']['category'] = category
                product_for_create.append(Product(**product['fields']))
            except Category.DoesNotExist:
                # Если категория не найдена, выводим сообщение
                self.stdout.write(self.style.WARNING(
                    f'Категория с pk {product["fields"]["category"]} не найдена. Продукт {product["fields"]["name"]} не будет создан.'
                ))

        # Создаем объекты в базе с помощью метода bulk_create()
        if product_for_create:
            Product.objects.bulk_create(product_for_create)
            self.stdout.write(self.style.SUCCESS('Продукты успешно созданы'))
        else:
            self.stdout.write(self.style.WARNING('Не было создано ни одного продукта'))
