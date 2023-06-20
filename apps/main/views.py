from django import TemplateView
from django import render


# Render IndexView
class IndexTemplateView(TemplateView):
    template_name = 'main/index.html'
    content_type = 'text/html'


# Render error_404_view
def error_404_view(request, exception):
    return render(request, 'main/404.html')
