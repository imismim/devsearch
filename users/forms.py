from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile, Skill, Message


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


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'short_intro', 'bio', 'profile_image',
                  'social_github', 'social_instagram', 'social_youtube', 'social_linkedin', 'social_website']

        labels = {}

    def clean_username(self):
        username = self.cleaned_data.get('username')

        qs = Profile.objects
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        qs = qs.filter(username=username)

        if qs.exists():
            raise ValidationError('This username exist!')

        return username

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update(
                {'class': 'input input--text', 'type': 'text', 'name': 'text',
                 'id': 'formInput#text'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'input input--text', 'type': 'text', 'name': 'text',
                 'id': 'formInput#text', 'placeholder':'Enter skill', 'valued': self.fields['name']})
        self.fields['description'].widget.attrs.update({'class': 'input input--text', 'type': 'text', 'name': 'text',
                 'id': 'formInput#text', 'placeholder': 'Enter description',})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
    
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update(
                {'class': 'input input--text', 'type': 'text', 'name': 'text',
                 'id': 'formInput#text'})