from django import forms
from .models import Instructor, Course, Student
from django.contrib.auth.models import User


class InstructorForm(forms.ModelForm):
	class Meta:
		model = Instructor
		fields = ['user', 'course']

class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username']