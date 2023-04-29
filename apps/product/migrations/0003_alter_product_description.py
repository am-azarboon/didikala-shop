# Generated by Django 4.2 on 2023-04-29 13:06

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_product_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=ckeditor.fields.RichTextField(
                blank=True, null=True, verbose_name="Description"
            ),
        ),
    ]
