from django.views.generic import TemplateView
# Create your views here.
class Blog(TemplateView):
    template_name = "blog/home.html"