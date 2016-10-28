from django.shortcuts import render
from .models import Instructor, Course, Student
from django.urls import reverse
from django.views import generic
from .forms import InstructorForm, LoginForm
from django.contrib.auth.models import User

# Create your views here.

class IndexView(generic.FormView):
	template_name = "feeder/index.html"
	form_class = LoginForm
	success_url = '/feeder/index'

class RegisterView(generic.FormView):
	template_name = "feeder/register.html"
	form_class = InstructorForm
	success_url = '/feeder/index'

def AddSession(request):
	try:
		user = User.objects.get(username=request.POST['username'])
	except (KeyError, User.DoesNotExist) :
		return render(request, "feeder/index.html", {
				'error_message' : "Wrong username",
			})
	else:
		welcome = "Welcome, " + user.get_full_name()
		return render(request, "feeder/index.html", {
				'error_message' : welcome
			})


