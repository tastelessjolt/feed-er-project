from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from feeder.models import Instructor, Course, Student
from django.urls import reverse
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
# Create your views here.

def LoginView(request):
	error_message=''
	if request.method == "POST":
		form = LoginForm(request.POST)
		# if form.is_valid():
		user = authenticate(username=request.POST['email'], password=request.POST['password'])
		if user is not None:
			if user.is_superuser:
				login(request, user)
				welcome = "Welcome, " + user.get_full_name()
				return render(request, "admins/index.html", {
					'error_message' : welcome
				})
			else :
				error_message='You are not an admin'
		else :
			form = LoginForm(request.POST)
			error_message='Wrong email or password'
				
	else :
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('admins:index'))
		else :
			form = LoginForm()
	return render(request, "admins/login.html", {
			'form' : form, 
			'error_message' : error_message
		 } )

@permission_required('is_superuser', raise_exception=True)
def IndexView(request):
	return render(request, "admins/index.html", {'user' : request.user })

@login_required
def Logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('admins:login'))
