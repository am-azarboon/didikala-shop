from django import post_save
from django import receiver
from .models import Product, ProductCustom


# Save selling_counts by signals
@receiver(post_save, sender=ProductCustom)
def product_custom_saved(sender, instance, created, *args, **kwargs):
    product = Product.objects.get(product_custom=instance)  # Get current Product
    quantity = 0  # Set a default quantity

    for custom in product.product_custom.all():  # Iterate all custom products in current product
        quantity += custom.quantity  # Add each custom product count

    product.selling_counts = quantity  # Save all selling counts as product's selling_count
    product.save()
