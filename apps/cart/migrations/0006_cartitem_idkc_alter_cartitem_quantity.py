# Generated by Django 4.2 on 2023-05-03 13:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0005_alter_cart_total_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="idkc",
            field=models.BigIntegerField(
                default=0, editable=False, verbose_name="idkc"
            ),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="quantity",
            field=models.PositiveIntegerField(default=0, verbose_name="Quantity"),
        ),
    ]