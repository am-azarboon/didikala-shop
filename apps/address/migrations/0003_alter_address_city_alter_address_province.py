# Generated by Django 4.2 on 2023-05-19 08:52

from django import migrations, models
import django


class Migration(migrations.Migration):
    dependencies = [
        ("address", "0002_remove_address_firstname_remove_address_lastname_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="city",
            field=models.ForeignKey(
                max_length=32,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="address.city",
                verbose_name="City",
            ),
        ),
        migrations.AlterField(
            model_name="address",
            name="province",
            field=models.ForeignKey(
                max_length=32,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="address.province",
                verbose_name="Province",
            ),
        ),
    ]
