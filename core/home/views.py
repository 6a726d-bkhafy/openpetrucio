from django.views.generic import TemplateView
from . import urls

# Create your views here.

class DashView(TemplateView):
    template_name='dash.html'