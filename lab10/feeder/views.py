from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404,get_list_or_404, Http404
from .models import *
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .forms import *
from http.cookies import CookieError
from admins.forms import QuestionForm
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core import serializers
from django.forms import formset_factory
import urllib.request
import json, logging
import datetime
# Create your views here.

logger = logging.getLogger('django')

@csrf_exempt
def StudentLogin(request):
	# logger.info(request)
	if request.method == "GET":
		return render(request, 'feeder/csrf.html')
	elif request.method == "POST" :
		logger.info(str(request));
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			if hasattr(user, 'student'):
				login(request, user)
				response = HttpResponse('No id cookie! Sending cookie to client')
				response.set_cookie('sessionid', request.COOKIES.get('sessionid'), secure=True, expires = timezone.now() + datetime.timedelta(days=365))
				return response
			return HttpResponse("You are not allowed here")
		return HttpResponse("Wrong username or password")

@csrf_exempt
@login_required
def APIendpoint(request):
	JSONSerializer = serializers.get_serializer("json")
	if request.method == "POST":
		logger.info(request.POST.get('q'))
		if request.POST.get('q') == 'getcourses' :
			courses = request.user.student.course.all();
			response = HttpResponse(serializers.serialize("json", courses), content_type='application/json')
		elif request.POST.get('q') == 'getfeedbackforms' :
			fq = Feedback.objects.none()
			for c in request.user.student.course.all():
				fq = fq | c.feedback_set.all()
			response = HttpResponse(serializers.serialize("json", fq), content_type='application/json')
		elif request.POST.get('q') == 'getassignemnts' :
			aq = Assignment.objects.none()
			for c in request.user.student.course.all():
				aq = aq | c.assignment_set.all()
			response = HttpResponse(serializers.serialize("json", aq), content_type='application/json')
		elif request.POST.get('q') == 'getquestions':
			qq = Question.objects.none();
			for c in request.user.student.course.all():
				for f in c.feedback_set.all() :
					qq = qq | f.question_set.all()
			response = HttpResponse(serializers.serialize("json", qq), content_type='application/json')
		response.set_cookie('sessionid', request.COOKIES.get('sessionid'), secure=True, expires = timezone.now() + datetime.timedelta(days=365))
		return response
	elif request.method == "GET":
		fq = Feedback.objects.none()
		for c in request.user.student.course.all():
			fq = fq | c.feedback_set.all()

		data = serializers.serialize("json", fq)
		response = HttpResponse(data, content_type='application/json')
		response.set_cookie('sessionid', request.COOKIES.get('sessionid'), secure=True, expires = timezone.now() + datetime.timedelta(days=365))
		return response

def TestAPI(request):
	# JSONSerializer = serializers.get_serializer("json")
	aq = Assignment.objects.none()
	for c in Course.objects.all():
		aq = aq | c.assignment_set.all()
	response = HttpResponse(serializers.serialize("json", aq), content_type='application/json')
	return response

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

@login_required(login_url='/feeder/login/')
def IndexView(request):
	courses = Course.objects.all()
	assignments = Assignment.objects.filter(deadline__gt=timezone.now()).order_by('deadline')
	context = {
		'user' : request.user,
		'courses' : courses,
		'assignments' : assignments,
		}
	return render(request, "feeder/index.html", context)

@login_required(login_url='/feeder/login/')
def Logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('feeder:login'))

@login_required(login_url='/feeder/login/')
def AddFeedback(request):
	if request.method == "POST":
		error_message=''
		fb = FeedbackForm(request.POST)
		QuestionFormSet = formset_factory(QuestionForm)
		qsformset = QuestionFormSet(request.POST)
		if fb.is_valid() :
			if qsformset.is_valid() :
				feedback = fb.save(commit=False)
				feedback.pub_date = timezone.now()
				feedback.save()
				for qsform in qsformset :
					question = qsform.save(commit=False)
					question.feedback_id = feedback.id
					question.save()  
				return render(request, 'feeder/in_success.html', { 'message' : 'Feedback form created successfully' })
			else :
				error_message='Invalid questions'
		else :
			error_message='Invalid feedback form data' 
		context = { 
			'fb' : fb,
			'qsformset' : qsformset,
			'error_message' : error_message,
 		}
		return render(request, 'feeder/add_feedback.html', context)
	else :
		fb = FeedbackForm()
		QuestionFormSet = formset_factory(QuestionForm)
		qsformset = QuestionFormSet()
		context = { 
			'fb' : fb,
			'qsformset' : qsformset,
 		}
		return render(request,'feeder/add_feedback.html', context)
@login_required(login_url='/feeder/login')
def AllFeedbacks(request):
	feedbacks = Feedback.objects.filter(deadline__gt=timezone.now()).order_by('deadline')
	old_feedbacks = Feedback.objects.filter(deadline__lt=timezone.now()).order_by('deadline').reverse()
	context = {
		'feedbacks' : feedbacks,
		'old_feedbacks' : old_feedbacks,
	}
	return render(request, 'feeder/feedbacks.html', context)

@login_required(login_url='/feeder/login')
def FeedbackView(request, pk):
	feedback = get_object_or_404(Feedback, pk = pk)
	questions = feedback.question_set.all()
	noneAnswer = Answer.objects.all()
	context = {
		'feedback' : feedback,
		'questions' : questions,
		# 'noneAnswer' : ,
	}
	return render(request, 'feeder/feedback.html', context)

@login_required(login_url='/feeder/login')
def AddAssignment(request):
	error_message=''
	if request.method == 'POST' :
		assignform = AssignmentForm(request.POST)
		if assignform.is_valid() :
			assign = assignform.save(commit = False)
			assign.pub_date = timezone.now()
			assign.save()
			return render(request,'feeder/in_success.html', {'message' : 'Assignment/Exam created and deadline set successfully'})
		else :	
			error_message='Invalid data'
		context = {
			'assignform' : assignform,
			'error_message' : error_message,
		}
		return render(request, 'feeder/add_assignment.html', context)
	else :
		assignform = AssignmentForm()
		context = {
			'assignform' : assignform,
		}
		return render(request, 'feeder/add_assignment.html', context)


@login_required(login_url='/feeder/login')
def AllAssignments(request):
	assignments = Assignment.objects.filter(deadline__gt=timezone.now()).order_by('deadline')
	old_assignments = Assignment.objects.filter(deadline__lt=timezone.now()).order_by('deadline').reverse()
	context = {
		'assignments' : assignments,
		'old_assignments' : old_assignments,
	}
	return render(request, 'feeder/assignments.html', context)

@login_required(login_url='/feeder/login')
def AssignmentView(request,pk):
	assignment = get_object_or_404(Assignment,pk = pk)
	return render(request, 'feeder/assignment.html', {'assignment' : assignment})

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
