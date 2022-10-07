from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Files
from django import forms

class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

class FileForm(ModelForm):
	class Meta:
		model = Files
		fields = ['file']