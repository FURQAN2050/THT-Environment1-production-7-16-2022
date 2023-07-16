from django.urls import path
from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('api/data/', views.WorkoutAPI.as_view()),
]