from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name:',
            'email': 'Email:',
            'username': 'Username:',
            'password1': 'Password:',
            'password2': 'Repeat password:'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update(
            {'class': 'input input--text', 'type': 'text', 'name': 'text',
             'id': 'formInput#text', 'placeholder': 'e.g. Arsen Korytskyi'})
        self.fields['email'].widget.attrs.update(
            {'class': 'input input--email', 'type': 'email', 'name': 'email',
             'id': 'formInput#email', 'placeholder': 'e.g. user@domain.com'})
        self.fields['username'].widget.attrs.update(
            {'class': 'input input--text', 'type': 'text', 'name': 'text',
             'id': 'formInput#text', 'placeholder': 'e.g. arsenkorytskyi'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'input input--password', 'type': 'password', 'name': 'password',
             'id': 'formInput#passowrd', 'placeholder': '••••••••'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'input input--password', 'type': 'password', 'name': 'password',
             'id': 'formInput#passowrd', 'placeholder': '••••••••'})
