from django.urls import path
from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', login_required(views.MainBoardView.as_view()), name='board'),
    path('', views.redirect_view),
    path('board/api/data/', views.PointsData.as_view()),
]