from django import forms
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm, UserCreationForm

from .models import User


class SignupForm(UserCreationForm):
    """Cadastro pelo site: e-mail, nome e senha."""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class CustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)
