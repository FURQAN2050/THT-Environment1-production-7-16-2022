from django.urls import path
from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from .views import GoalAPI
from django.views.generic import TemplateView


urlpatterns = [
    path('api/data/', GoalAPI.as_view()),
]