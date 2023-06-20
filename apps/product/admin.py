from django.contrib.auth.models import models as a_model
from django.contrib import admin
from django import forms
from . import models


# Register Color Model
@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('title_fa', 'title_en', 'hex_code',)
    list_display_links = ('title_fa', 'title_en')


# Register Size model
@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)


# Register ProductImage as inline
class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 0


# Register ProductImage
@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt', 'show_image')


# Register ProductCustom as inline
class ProductCustomInline(admin.StackedInline):
    model = models.ProductCustom
    extra = 0

    # Change formField attributes(size)
    formfield_overrides = {
        a_model.IntegerField: {'widget': forms.NumberInput(attrs={'size': '20'})},
    }


# Register Product
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('idk', 'title',)
    list_display_links = ('idk', 'title',)
    search_fields = ('idk', 'title',)
    inlines = (ProductImageInline, ProductCustomInline)

    # Change formField attributes(size)
    formfield_overrides = {
        a_model.CharField: {'widget': forms.TextInput(attrs={'size': '90'})},
    }
