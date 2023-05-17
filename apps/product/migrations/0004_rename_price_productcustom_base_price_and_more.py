# Generated by Django 4.2 on 2023-04-30 14:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0003_alter_product_description"),
    ]

    operations = [
        migrations.RenameField(
            model_name="productcustom",
            old_name="price",
            new_name="base_price",
        ),
        migrations.AddField(
            model_name="productcustom",
            name="selling_price",
            field=models.IntegerField(
                default=0, editable=False, null=True, verbose_name="Selling price"
            ),
        ),
        migrations.AlterField(
            model_name="productcustom",
            name="slug",
            field=models.SlugField(
                allow_unicode=True, blank=True, editable=False, verbose_name="Slug"
            ),
        ),
    ]