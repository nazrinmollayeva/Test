# Generated by Django 5.1.7 on 2025-04-12 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_category_products_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='brand',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
