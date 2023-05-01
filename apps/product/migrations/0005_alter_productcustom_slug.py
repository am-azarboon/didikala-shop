# Generated by Django 4.2 on 2023-04-30 14:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0004_rename_price_productcustom_base_price_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productcustom",
            name="slug",
            field=models.SlugField(
                allow_unicode=True,
                blank=True,
                editable=False,
                max_length=32,
                verbose_name="Slug",
            ),
        ),
    ]
