from django.urls import path, include
from django.views.generic import TemplateView

from .views import EmailVerify, CustomLoginView, Register


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', Register.as_view(), name='signup'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(),
         name='verify_email'),
    path('confirm_email/',
         TemplateView.as_view(template_name='verify/confirm_email.html'),
         name='confirm_email'),
    path('complete_verify/',
         TemplateView.as_view(template_name='verify/complete_verify.html'),
         name='complete_verify'),
    path('invalid_verify/',
         TemplateView.as_view(template_name='verify/invalid_verify.html'),
         name='invalid_verify'),
]
