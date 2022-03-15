from django.forms import ModelForm, fields, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class AnswerForm(ModelForm):
    class Meta:
        model=Answer
        fields=('detail',)

        widgets={
            'detail': forms.TextInput(attrs={'class': 'form-control','placeholder':'Write Answer...'}),
        }

class QuestionForm(ModelForm):
    class Meta:
        model=Question
        fields=('q_title','detail','tags')

        widgets={
            'q_title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Question Title...'}),
            'detail': forms.TextInput(attrs={'class': 'form-control','placeholder':'Question Detail...'}),
            'tags': forms.TextInput(attrs={'class': 'form-control','placeholder':'Question Related Tags...'}),
        }

class ProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        fields='__all__'
        exclude = ['user']
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Name...'}),
            'phone': forms.TextInput(attrs={'class': 'form-control','placeholder':'Phone Number...'}),
            'email': forms.TextInput(attrs={'class': 'form-control','placeholder':'Email...'}),
            'address': forms.TextInput(attrs={'class': 'form-control','placeholder':'Adress...'}),
        }