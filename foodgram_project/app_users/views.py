from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator

from .models import User
from .forms import CreationForm, AuthForm
from .utils import send_email_for_verify


class CustomLoginView(LoginView):
    form_class = AuthForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        check_token = default_token_generator.check_token(user, token)
        if user is not None and check_token:
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('complete_verify')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
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
            #first_name = form.cleaned_data['first_name']
            #last_name = form.cleaned_data['last_name']
            user = authenticate(email=email, username=username, password=password)
            print('>>>>>>>>>>>>>>>>>>>>')
            print(user)
            send_email_for_verify(request, user)
            return redirect('confirm_email')

        return render(request, self.template_name, {'form': form})


def register_user(request):
    form = CreationForm()

    if request.method == 'POST':
        form = CreationForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            is_active=False)

            send_email_for_verify(request, user)
            return redirect('confirm_email')
    return render(request, 'signup.html', {'form':form})
