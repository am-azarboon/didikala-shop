from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.utils.html import format_html
from django.utils.text import slugify
from django.shortcuts import reverse
from django.db import models


# Color model
class Color(models.Model):
    title_fa = models.CharField(_('Title Fa'), max_length=32)
    title_en = models.CharField(_('Title En'), max_length=32, null=True, blank=True)
    hex_code = models.CharField(_('Hex Code'), max_length=6, help_text=_('Example (001100)'))

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')

    def __str__(self):
        return f"{self.title_fa} - {self.hex_code}"


# Size model
class Size(models.Model):
    title = models.CharField(_('Title'), max_length=64, help_text=_('Example (XL)'))

    class Meta:
        verbose_name = _('Size')
        verbose_name_plural = _('Sizes')

    def __str__(self):
        return self.title


# Product model
class Product(models.Model):
    idk = models.BigAutoField(primary_key=True)
    title = models.CharField(_('Product Title'), max_length=128)
    videos = models.FileField(_('Product Video'), upload_to='video/products', null=True, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    description = RichTextField(_('Description'), null=True, blank=True)
    selling_counts = models.PositiveIntegerField(_('Selling counts'), default=0, null=True, editable=False)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ('idk',)

    def __str__(self):
        return self.title


# ProductCustom model
class ProductCustom(models.Model):
    idkc = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, verbose_name=_('Main product'), on_delete=models.CASCADE, related_name='product_custom')
    price = models.IntegerField(_('Price'), help_text=_('Rials'), default=0)
    discount = models.PositiveIntegerField(_('Discount'), help_text=_('Percentage(%)'), default=0)
    counts = models.PositiveIntegerField(_('Counts'), default=0)
    slug = models.SlugField(_('Slug'), blank=True, editable=False)

    color = models.ForeignKey(Color, verbose_name=_('Color'), null=True, blank=True, on_delete=models.DO_NOTHING, related_name='product_custom')
    size = models.ForeignKey(Size, verbose_name=_('Size'), null=True, blank=True, on_delete=models.DO_NOTHING, related_name='product_custom')

    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created time'), auto_now=True)

    class Meta:
        verbose_name = _('Custom product')
        verbose_name_plural = _('Custom products')
        ordering = ('idkc',)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.product.title)
        super(ProductCustom, self).save()

    def get_absolute_url(self):
        return reverse('product:detail', args=[self.idkc])

    def __str__(self):
        return f"{self.idkc} - {self.product}"


# ProductImage model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(_('Image'), upload_to='image/products')
    alt = models.CharField(_('Short Description'), max_length=32)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def show_image(self):
        return format_html(f'<img src="{self.image.url}" width="78px" height="42px" alt="none">')

    def __str__(self):
        return self.alt
