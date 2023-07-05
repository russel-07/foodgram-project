from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

from .utils import send_email_for_verify


User = get_user_model()


class AuthForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if not self.user_cache.is_active:
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError(
                    'Вам необходимо верифицировать email. Проверьте почту!',
                    code='invalid_login'
                    )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
