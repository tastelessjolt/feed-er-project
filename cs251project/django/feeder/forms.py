from django import forms
from .models import *
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

class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		exclude = ['pub_date']
		widgets = {
			'deadline' : forms.DateTimeInput(attrs={'class':'date-format'}),
		}

class AssignmentForm(forms.ModelForm):
	class Meta:
		model = Assignment
		exclude = ['pub_date']
		widgets = {
			'deadline' : forms.DateTimeInput(attrs={'class':'date-format'}),
		}