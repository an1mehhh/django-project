# Generated by Django 4.2 on 2024-07-28 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_product_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Публикация'),
        ),
    ]