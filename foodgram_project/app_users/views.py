from django.views.generic import CreateView
from django.urls import reverse_lazy

from . import forms


class SignUp(CreateView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


