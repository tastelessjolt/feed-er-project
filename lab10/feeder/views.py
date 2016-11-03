from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Instructor, Course, Student
from django.urls import reverse
from django.views import generic
from .forms import InstructorForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
import urllib.request
import json	
# Create your views here.

def StudentLogin(request):
	if request.method == "GET":
		return HttpResponse("Yoo. You GET me. :P")
	else :
		user = authenticate(username=request.POST['email'], password=request.POST['password'])
		if user is not None:
			if hasattr(user, 'student'):
				login(request, user)
				return HttpResponse(json(user))
			return HttpResponse(json(('message',"You are not allowed here")))
		return HttpResponse(json(('message',"Wrong username or password")))


def LoginView(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		# if form.is_valid():
		if request.POST.get('token'):
			user = authenticate(token = request.POST['token'])
		else :
			user = authenticate(username=request.POST['email'], password=request.POST['password'])
		if user is not None:
			if hasattr(user, 'instructor'):
				login(request, user)
				welcome = "Welcome, " + user.get_full_name()
				return render(request, "feeder/index.html", {
					'error_message' : welcome,
				})
			else :
				return HttpResponseRedirect(reverse('feeder:login'))
		else :
			form = LoginForm(request.POST)
			return render(request, "feeder/login.html", {
				'form' : form,
				'error_message' : "Wrong email or password",
			})
				
	else :
		if request.user.is_authenticated :
			return HttpResponseRedirect(reverse('feeder:index'))
		else :
			form = LoginForm()
	return render(request, "feeder/login.html", {'form' : form  } )
# @login_required(login_url='/feeder/login/')

@permission_required('not is_superuser', login_url='/feeder/login/')
def IndexView(request):
	return render(request, "feeder/index.html", {'user' : request.user })

@login_required(login_url='/feeder/login/')
def Logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('feeder:login'))

def RegisterView(request):
	if request.method == "POST":
		form = InstructorForm(request.POST)
		if form.is_valid():
			try: 
				User.objects.get(username=request.POST['email'])
			except (KeyError, User.DoesNotExist):
				user = User()
				instructor = Instructor()
				user.first_name=request.POST['first_name']
				user.last_name=request.POST['last_name']
				user.username=request.POST['email']
				user.set_password(request.POST['password'])
				user.save()
				instructor.user_id = user.id
				instructor.save()
				message = "Registration complete. You can now login"
				return render(request,'feeder/success.html')
			else :
				error_message="This email has already been taken"
	else :
		form = InstructorForm()
		error_message=''
	return render(request, 'feeder/register.html',{
			'form' : form,
			'error_message' : error_message,
		})


def TokenVerify(request):
	CLIENT_ID = "410381470-aviccs0f691gm6eqin9k9opo3ko5sji6.apps.googleusercontent.com"
	validation_url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="
	if request.method == 'POST':
		token = request.POST['idtoken']
		data = json.loads(urllib.request.urlopen(validation_url + token).read().decode('utf-8'))
		# return HttpResponse(str(type(data)))
		if data['aud'] == CLIENT_ID:
			if data['iss'] in ['accounts.google.com', 'https://accounts.google.com']:
				return HttpResponse(data['exp'])

		return data

	else:
		return 
