from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForm


from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .utils import send_email_for_verify


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class EmailVerify():
    pass


def register_user(request):
    form = CreationForm()

    if request.method == 'POST':
        form = CreationForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            user_email = form.cleaned_data['email']
            user_username = form.cleaned_data['username']
            user_password = form.cleaned_data['password1']

            # Create new user
            user = User.objects.create_user(username=user_username, email=user_email, password=user_password)

            # Make user unactive until they click link to token in email
            user.is_active = False 
            send_email_for_verify(request, user)
            return redirect('confirm_email')

    return render(request, 'signup.html', {'form':form})



