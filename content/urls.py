from django.urls import path
from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    path('', login_required(views.ContentViewPage.as_view()), name='board'),
    path('api/data/', views.ContentView.as_view()),
    path('api/search/', views.SearchView.as_view()),
]