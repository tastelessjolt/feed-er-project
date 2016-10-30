from django import forms
from django.contrib.auth.models import User
from feeder.models import Course, Instructor, Feedback, Question, Answer, Assignment

class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email', 'password']
		widgets = {
			'password' : forms.PasswordInput()
		}

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class InstructorForm(forms.ModelForm):
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	username = forms.EmailField()
	class Meta:
		model = Instructor
		fields = '__all__'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
    
class GetInstructorForm(forms.Form):
	first_name = User._meta.get_field('first_name').formfield()
	last_name = User._meta.get_field('last_name').formfield()
	email = User._meta.get_field('username').formfield()
	course = Instructor._meta.get_field('course').formfield()

class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		exclude = ['course','pub_date']
		widgets = {
			'deadline' : forms.DateInput(attrs={'class':'date-format'}),
		}

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		exclude = ['feedback']  

class AssignmentForm(forms.ModelForm):
	class Meta:
		model = Assignment
		exclude = ['pub_date', 'course']