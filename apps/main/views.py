from django.views.generic import TemplateView


# Render IndexView
class IndexTemplateView(TemplateView):
    template_name = 'main/index.html'
    content_type = 'text/html'
