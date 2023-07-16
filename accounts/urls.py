from django.urls import path
from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('success/', TemplateView.as_view(template_name='signup_success.html'), name='success'),
    path('selectschool/', views.SelectSchool.as_view(), name='selectschool'),
    path('finish/', views.FinishSignUp.as_view(), name='finish'),
    path('subscribe/', login_required(views.SubscribeView.as_view()), name='subscribe'),
    path('api/process_payment/', views.ProcessPayment.as_view(), name='process_payment'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('healthinfo/', login_required(views.HealthDataEnter.as_view()), name='healthinfo'),
    path('macros/', login_required(views.MacronutrientsView.as_view()), name='macros'),
    path('confirm/', TemplateView.as_view(template_name='signup_confirm.html'), name='confirm'),
    path('success_test/', TemplateView.as_view(template_name='success.html'), name='success_test'),
    path('api/data/', views.Teams.as_view()),
    path('profile/edit/', login_required(views.Profile.as_view()), name='edit_profile'),
    path('profile/edit/<str:currentTab>', login_required(views.Profile.as_view()), name='edit_profile'),
    path('profile/change-password', views.Password.as_view(), name='edit_password'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.Activate.as_view(), name='activate'),
    path('', views.redirect_view),
]