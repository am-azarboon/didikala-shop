# Generated by Django 4.2 on 2023-04-27 13:16

from django import migrations, models
import django


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Color",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title_fa", models.CharField(max_length=32, verbose_name="Title Fa")),
                (
                    "title_en",
                    models.CharField(
                        blank=True, max_length=32, null=True, verbose_name="Title En"
                    ),
                ),
                (
                    "hex_code",
                    models.CharField(
                        help_text="Example (001100)",
                        max_length=6,
                        verbose_name="Hex Code",
                    ),
                ),
            ],
            options={
                "verbose_name": "Color",
                "verbose_name_plural": "Colors",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("idk", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "title",
                    models.CharField(max_length=128, verbose_name="Product Title"),
                ),
                (
                    "videos",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="video/products",
                        verbose_name="Product Video",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "selling_counts",
                    models.PositiveIntegerField(
                        default=0,
                        editable=False,
                        null=True,
                        verbose_name="Selling counts",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
                "ordering": ("idk",),
            },
        ),
        migrations.CreateModel(
            name="Size",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Example (XL)", max_length=64, verbose_name="Title"
                    ),
                ),
            ],
            options={
                "verbose_name": "Size",
                "verbose_name_plural": "Sizes",
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to="image/products", verbose_name="Image"),
                ),
                (
                    "alt",
                    models.CharField(max_length=32, verbose_name="Short Description"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_image",
                        to="product.product",
                        verbose_name="Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Image",
                "verbose_name_plural": "Images",
            },
        ),
        migrations.CreateModel(
            name="ProductCustom",
            fields=[
                ("idkc", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "price",
                    models.IntegerField(
                        default=0, help_text="Rials", verbose_name="Price"
                    ),
                ),
                (
                    "discount",
                    models.PositiveIntegerField(
                        default=0, help_text="Percentage(%)", verbose_name="Discount"
                    ),
                ),
                (
                    "counts",
                    models.PositiveIntegerField(default=0, verbose_name="Counts"),
                ),
                (
                    "slug",
                    models.SlugField(blank=True, editable=False, verbose_name="Slug"),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "created_at",
                    models.DateTimeField(auto_now=True, verbose_name="Created time"),
                ),
                (
                    "color",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="product_custom",
                        to="product.color",
                        verbose_name="Color",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_custom",
                        to="product.product",
                        verbose_name="Main product",
                    ),
                ),
                (
                    "size",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="product_custom",
                        to="product.size",
                        verbose_name="Size",
                    ),
                ),
            ],
            options={
                "verbose_name": "Custom product",
                "verbose_name_plural": "Custom products",
                "ordering": ("idkc",),
            },
        ),
    ]
