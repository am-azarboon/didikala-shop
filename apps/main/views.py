from django.views.generic import TemplateView
from django.shortcuts import render


# Render IndexView
class IndexTemplateView(TemplateView):
    template_name = 'main/index.html'
    content_type = 'text/html'
