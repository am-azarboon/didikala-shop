from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, ProductCustom


# Save selling_counts by signals
@receiver(post_save, sender=ProductCustom)
def product_custom_saved(sender, instance, created, *args, **kwargs):
    product = Product.objects.get(product_custom=instance)  # Get current Product
    count = 0  # Set a default counter

    for custom in product.product_custom.all():  # Iterate all custom products in current product
        count += custom.counts  # Add each custom product count

    product.selling_counts = count  # Save all selling counts as product's selling_count
    product.save()
