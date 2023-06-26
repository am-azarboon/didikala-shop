from django.views.generic import DetailView, TemplateView, ListView
from apps.cart.cart import SessionCart, ModelCart
from .models import Product, ProductCustom, Category
from apps.cart.models import CartItem


# Render ProductDetailView
class ProductDetailView(DetailView):
    model = ProductCustom
    template_name = "product/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["in_cart"] = False

        # Check if user authenticated
        if self.request.user.is_authenticated:
            cart = ModelCart(self.request)

            # Check if product is in ModelCart
            if CartItem.objects.filter(product__idkc=self.kwargs.get("pk"), cart=cart.cart).exists():
                context["in_cart"] = True
        else:
            cart = SessionCart(self.request)  # Get the user cart from sessions

            # Send the added True to template if product is in SessionCart
            if str(self.kwargs.get("pk")) in cart.cart:
                context["in_cart"] = True

        return context


class CategorySearch(ListView):
    template_name = "product/products.html"
    context_object_name = "products"
    model = Product
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs["slug"]
        category = Category.objects.get(slug=slug)

        if category.sub_categories.all():
            return Product.objects.filter(category__parent__slug=slug)

        return Product.objects.filter(category__slug=slug)


# Render Navbar Menu
class NavbarMenuView(TemplateView):
    template_name = "includes/navbar_menu.html"

    def get_context_data(self, **kwargs):
        context = super(NavbarMenuView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        return context
