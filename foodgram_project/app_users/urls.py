from django.urls import path, include
from django.views.generic import TemplateView

from .views import SignUp, EmailVerify, register_user

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', SignUp.as_view(), name='signup'),


    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('confirm_email/',
         TemplateView.as_view(template_name='registration/confirm_email.html'),
         name='confirm_email'),
    path('register/', register_user, name='register'),
]
