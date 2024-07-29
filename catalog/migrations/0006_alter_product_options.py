# Generated by Django 4.2 on 2024-07-28 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name', 'description', 'price', 'created_at'), 'permissions': [('cancel_publication', 'Отмена публикации'), ('can_edit_description', 'Редактирование описания'), ('can_edit_category', 'Редактирование категории')], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
