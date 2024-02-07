import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from humans.models import News


def my_first_validator(value):
    if len(value) > 30:
        raise ValidationError(f'Будь краток, у тебя 30 символов! Лимит превышен на {len(value) - 30} симв.')


class FeedbackForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    message = forms.CharField(label='Сообщение',
                              validators=[my_first_validator],
                              widget=forms.Textarea(attrs={'cols': 50,
                                                           'rows': 5,
                                                           'style': 'color: red; font-size: 14px;'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            forbidden_domains_regex = r'\.com$|\.tw$'
            if re.search(forbidden_domains_regex, email, re.IGNORECASE):
                raise ValidationError('Использование данного домена запрещено')
        return "qaz" + email


class AddNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }


class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
