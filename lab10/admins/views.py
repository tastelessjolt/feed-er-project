from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404,get_list_or_404
from feeder.models import Instructor, Course, Student
from django.urls import reverse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.forms.models import model_to_dict
from django.forms import inlineformset_factory
from django.forms import formset_factory
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
				return HttpResponseRedirect(reverse('admins:index'))
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
			'error_message' : error_message,
		 } )

@permission_required('is_superuser', raise_exception=True)
def IndexView(request):
	return render(request, "admins/index.html", {
		'user' : request.user, 
		'instructors': Instructor.objects.all(), 
		'courses' : Course.objects.all()
	})

@permission_required('is_superuser', raise_exception=True)
def Logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('admins:login'))

@permission_required('is_superuser', raise_exception=True)
def AllCourses(request):
	return HttpResponse("Courses page")

@permission_required('is_superuser', raise_exception=True)
def GetCourse(request, pk):
	course = get_object_or_404(Course, pk=pk)
	UserFormSet = formset_factory(UserForm, extra=4)
	formset = UserFormSet()
	return render(request,'admins/course.html',{'formset' : formset})

@permission_required('is_superuser', raise_exception=True)
def AddCourse(request):
	if request.method == "POST":
		return HttpResponse("Nothing")
	else:
		courseform = CourseForm()
		fb = FeedbackForm
		AssignmentFormSet = formset_factory(AssignmentForm, extra=2)
		FeedbackFormSet = formset_factory(FeedbackForm, extra=2)
		asformset = AssignmentFormSet(initial=[{
			'assignment_name': 'Midsem Examination',
		}, {
			'assignment_name': 'Endsem Examination',
		}])
		fbformset  FeedbackFormSet()
		return render(request, "admins/add_course.html", {
				'cform' : courseform,
				'fbformset' : fbformset,
				'asformset' : asformset,
			})

@permission_required('is_superuser', raise_exception=True)
def AllInstructors(request):
	return HttpResponse()

@permission_required('is_superuser', raise_exception=True)
def GetInstructor(request, pk):
	instructor = get_object_or_404(Instructor,pk=pk)

	return render(request,'admins/course.html', {'form' : form })