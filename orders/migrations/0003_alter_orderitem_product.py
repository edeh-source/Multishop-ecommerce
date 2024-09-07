# Generated by Django 5.0.4 on 2024-07-10 08:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_delivered_order_paid'),
        ('shop', '0006_alter_review_product_alter_review_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='shop.product'),
        ),
    ]
