from django import forms
from .models import Instructor, Course, Student
from django.contrib.auth.models import User


class InstructorForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name' , 'email', 'password']
		widgets = {
			'password' : forms.PasswordInput()
		}


class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email', 'password']
		widgets = {
			'password' : forms.PasswordInput()
		}