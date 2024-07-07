from django.db import models

NULLABLE = {'blank': True, 'null': True}


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    image = models.ImageField(upload_to='image_products/', verbose_name="Изображение", **NULLABLE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за покупку", **NULLABLE)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    def __str__(self):
        return f'{self.name} {self.description} {self.price} {self.created_at}'

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ('name', 'description', 'price', 'created_at',)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание", **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ('name',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    version_number = models.CharField(max_length=50, verbose_name="Номер версии")
    version_name = models.CharField(max_length=100, verbose_name="Название версии")
    is_current_version = models.BooleanField(default=False, verbose_name="Текущая версия")

    def __str__(self):
        return f'{self.version_name} ({self.version_number})'

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ('-is_current_version', 'version_number',)
