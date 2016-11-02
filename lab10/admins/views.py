from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404,get_list_or_404, Http404
from feeder.models import Instructor, Course, Student, Feedback, Question
from django.urls import reverse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.forms.models import model_to_dict
from django.forms import formset_factory, inlineformset_factory
from django.utils import timezone
import logging
import csv, io, json

# Create your views here.

logger = logging.getLogger('django')

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
			usr = get_object_or_404(User, username=str(request.user))
			# return HttpResponse(usr.instructor)
			if not hasattr(usr, 'instructor') and not hasattr(usr, 'student') :
				return HttpResponseRedirect(reverse('admins:index'))
			else :
				error_message='You are not allowed here.'
		form = LoginForm()
	return render(request, "admins/login.html", {
			'form' : form, 
			'error_message' : error_message,
		 } )

@permission_required('is_superuser', login_url='/admins/login/')
def IndexView(request):
	return render(request, "admins/index.html", {
		'user' : request.user, 
		'instructors': Instructor.objects.all(), 
		'courses' : Course.objects.all(),
		'assignments' : Assignment.objects.order_by('deadline'),
		'feedbacks' : Feedback.objects.order_by('deadline'),
	})

@permission_required('is_superuser', login_url='/admins/login/')
def Logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('admins:login'))

@permission_required('is_superuser', login_url='/admins/login/')
def AllCourses(request):
	return HttpResponse("Courses page")

@permission_required('is_superuser', login_url='/admins/login/')
def GetCourse(request, pk):
	course = get_object_or_404(Course, pk=pk)
	courseform =  CourseForm(instance=course)
	studentlist = course.student_set.all()
	instructorlist = course.instructor_set.all()
	allstudents = Student.objects.all()
	allinstructors = Instructor.objects.all()
	# alldeadlines = course.feedback_set.all() | course.assignment_set.all()
	if request.method == "POST":
		st = ""
		for stud in studentlist :
			course.student_set.remove(stud)
		for inst in instructorlist :
			course.instructor_set.remove(inst)
		for value in request.POST:
			if value.startswith('student'):
				if request.POST[value] == 'on':
					value = value[7:]
					stud = get_object_or_404(Student, id=int(value))	
					stud.course.add(course)
				else :
					value = value[7:]
					stud = get_object_or_404(Student, id=int(value))	
					stud.course.remove(course)
			elif value.startswith('instructor'):
				if request.POST[value] == 'on':
					value = value[10:]
					inst = get_object_or_404(Instructor, id=int(value))	
					inst.course.add(course)
				else :
					value = value[10:]
					inst = get_object_or_404(Instructor, id=int(value))	
					inst.course.remove(course)
		return HttpResponseRedirect(reverse('admins:course', args={course.id, }))
	else :
		return render(request,'admins/course.html',{
			'cform' : courseform,
			'studentlist' : studentlist,
			'instructorlist' : instructorlist,
			'allstudents' : allstudents,
			'allinstructors' : allinstructors,
			# 'alldeadlines' : alldeadlines,
			'course' : course,
		})

@permission_required('is_superuser', login_url='/admins/login/')
def AddCourse(request):
	if request.method == "POST":
		AssignmentFormSet = formset_factory(AssignmentForm)
		FeedbackFormSet = formset_factory(FeedbackForm)
		QuestionFormSet = formset_factory(QuestionForm)
		
		courseform = CourseForm(request.POST)
		asformset = AssignmentFormSet(request.POST,prefix='as')
		fbform1 = FeedbackForm(request.POST, prefix='fb1')
		fbform2 = FeedbackForm(request.POST, prefix='fb2')
		qsformset1 = QuestionFormSet(request.POST, prefix='qs1')
		qsformset2 = QuestionFormSet(request.POST, prefix='qs2')
		
		if courseform.has_changed() or fbform1.has_changed() or fbform2.has_changed() or asformset.has_changed() or qsformset1.has_changed() or qsformset2.has_changed() :
			if courseform.is_valid() and fbform1.is_valid() and fbform2.is_valid() and asformset.is_valid() and qsformset1.is_valid() and qsformset2.is_valid() :
				qsformset1.is_valid()	
				qsformset2.is_valid()
				course = courseform.save()
				for asform in asformset :
					assign = asform.save(commit=False)
					assign.course_id = course.id
					assign.pub_date = timezone.now()
					assign.save()
				fb1 = fbform1.save(commit=False)
				fb2 = fbform2.save(commit=False)
				fb1.course_id = course.id
				fb1.pub_date = timezone.now()
				fb1.save()
				for qsform in qsformset1 :
					qs = qsform.save(commit=False)
					qs.feedback_id = fb1.id
					qs.save()
				fb2.course_id = course.id
				fb2.pub_date = timezone.now()
				fb2.save()
				for qsform in qsformset2 :
					qs = qsform.save(commit=False)
					qs.feedback_id = fb2.id
					qs.save()
				return render(request,'admins/success.html', {'message' : "Course has been registered"})

		return render(request,'admins/add_course.html',{
				'cform' : courseform,
				'fbform1' : fbform1,
				'fbform2' : fbform2,
				'asformset' : asformset,
				'qsformset1' : qsformset1,
				'qsformset2' : qsformset2,
			})
	else:
		courseform = CourseForm(initial={
			'course_code' : 'CS 251',
			'course_name' : 'Software Systems Lab',
			})
		fb = FeedbackForm
		AssignmentFormSet = formset_factory(AssignmentForm, extra=0)
		FeedbackFormSet = formset_factory(FeedbackForm, extra=0)
		QuestionFormSet = formset_factory(QuestionForm)


		asformset = AssignmentFormSet(prefix = 'as',initial=[{
			'assignment_name': 'Midsem Examination',
		}, {
			'assignment_name': 'Endsem Examination',
		}])

		fbform1 = FeedbackForm(prefix = 'fb1', initial={
			'fb_name': 'Midsem Examination',
		})
		fbform2 = FeedbackForm(prefix = 'fb2', initial={
			'fb_name': 'Endsem Examination',
		})

		qsformset1 = QuestionFormSet(prefix = 'qs1')
		qsformset2 = QuestionFormSet(prefix = 'qs2')

		return render(request, "admins/add_course.html", {
				'cform' : courseform,
				'fbform1' : fbform1,
				'fbform2' : fbform2,
				'asformset' : asformset,
				'qsformset1' : qsformset1,
				'qsformset2' : qsformset2,
			})

@permission_required('is_superuser', login_url='/admins/login/')
def AllInstructors(request):
	return HttpResponse()

@permission_required('is_superuser', login_url='/admins/login/')
def GetInstructor(request, pk):
	instructor = get_object_or_404(Instructor,pk=pk)
	crs =  [x.course_code for x in instructor.course.all()]
	init = { 
		'first_name' : instructor.user.first_name ,
		'last_name' : instructor.user.last_name ,
		'email' : instructor.user.username ,
		'course' : crs ,
	}
	if request.method == "POST" :
		iform = GetInstructorForm(request.POST, initial=init)
		# st = ''
		# for i in request.POST.get('course') :
		# 	st = st + ', ' + User.objects.get(pk=i).__str__()
		# return HttpResponse( st )
		if iform.has_changed():
			if iform.is_valid():
				instructor.user.first_name = iform.cleaned_data['first_name']
				instructor.user.last_name = iform.cleaned_data['last_name']
				instructor.user.username = iform.cleaned_data['email']
				for x in instructor.course.all():
					instructor.course.remove(x)
				for x in iform.cleaned_data['course']:
					instructor.course.add(x)
	else :
		iform = GetInstructorForm(initial=init)
	return render(request,'admins/instructor.html', {'iform' : iform })

@permission_required('is_superuser', login_url='/admins/login/')
def AddStudent(request):
	error_message=''
	if request.method == "POST":
		form = StudentForm(request.POST)
		# logger.info(User.objects.get(username=request.POST.get('username')))
		if form.is_valid():
			try: 
				User.objects.get(username=request.POST.get('username'))
			except (KeyError, User.DoesNotExist):
				user = User()
				student = Student()
				user.first_name=form.cleaned_data['first_name']
				user.last_name=form.cleaned_data['last_name']
				user.username=form.cleaned_data['username']
				user.set_password(form.cleaned_data['password'])
				user.save()
				student.user_id = user.id
				student.roll_no = form.cleaned_data['roll_no']
				student.save()
				message = "Student Registration Successful"
				return render(request,'admins/success.html', {'message' : message})
			else :
				error_message="This username has already been taken"
	else :
		form = StudentForm()
	return render(request, 'admins/add_student.html',{
			'form' : form,
			# 'rollform' : rollform
			'error_message' : error_message,
		})

@permission_required('is_superuser', login_url='/admins/login/')
def AddStudents(request):
	if request.method == 'POST':
		logger.info(request.FILES.get('csv_file'))
		students = io.TextIOWrapper(request.FILES['csv_file'].file)
		not_valid = ""
		for row in students :
			row = row.split(',')
			# return HttpResponse(row)
			try: 
				User.objects.get(username=row[3])
			except (KeyError, User.DoesNotExist):
				user = User(first_name=row[0], last_name=row[1], username=row[3])
				form = StudentForm(instance=user)
				form.is_valid()
				if form.errors == {} :
					user.set_password(row[4])
					user.save()
					student = Student()
					student.user_id = user.id
					student.roll_no = row[2]
					student.save()
				else :
					logger.info("It has Errors ")
					not_valid = not_valid + ", <br> " + str(row[3])
			else :
				logger.info("User already there")
				not_valid = not_valid + ", <br>" + str(row[3])

		if not_valid == "" :
			message = "All students successfully added"
		else :
			message = "Students addition unsuccessful. Check the csv file format. And Try again." + not_valid

		return render(request,'admins/success.html', {
			'message' : message,
			})
	else:
		form = AddStudentsForm()
		return render(request,'admins/add_students.html', {
			'form' : form,
			})