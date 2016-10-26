from django.shortcuts import render
from .models import Instructor, Course, Student
from django.urls import reverse
from django.views import generic
from django import forms

# Create your views here.

class InstructorForm(forms.ModelForm):
	class Meta:
		model = Instructor
		fields = ['first_name', 'second_name', 'email', 'course']

class IndexView(generic.DetailView):
	model = Instructor
	template_name = "feeder/index.html"

class RegisterView(generic.FormView):
	template_name = "feeder/register.html"
	form_class = InstructorForm
	# template_values['key'] =  "value" 
	success_url = '/feeder/index'
