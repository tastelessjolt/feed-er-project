from django import forms
from .models import Instructor, Course, Student


class InstructorForm(forms.ModelForm):
	class Meta:
		model = Instructor
		fields = ['first_name', 'second_name', 'email', 'course']

class LoginForm(forms.ModelForm):
	class Meta:
		model = Instructor
		fields = ['email']