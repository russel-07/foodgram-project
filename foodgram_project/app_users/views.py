from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.views import View

from .models import User
from .forms import CreationForm, AuthForm
from .utils import send_email_for_verify


class CustomLoginView(LoginView):
    form_class = AuthForm


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        check_token = default_token_generator.check_token(user, token)
        if user is not None and check_token:
            user.email_verify = True
            user.save()
            # from django.contrib.auth import login
            # login(request, user)
            return redirect('complete_verify')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class Register(View):
    template_name = 'signup.html'

    def get(self, request):
        form = CreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, username=username,
                                password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')

        return render(request, self.template_name, {'form': form})
