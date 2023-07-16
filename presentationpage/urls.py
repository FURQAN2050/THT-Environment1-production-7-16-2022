from django.urls import path
from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('presentation/', login_required(TemplateView.as_view(template_name='presentationpage/presentation_page.html')), name='presentation'),
    path('intro/', TemplateView.as_view(template_name='presentationpage/intro_page.html'), name='intro'),
]