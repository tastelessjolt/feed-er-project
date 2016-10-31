from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, UserManager, BaseUserManager

# Create your models here.


class Course(models.Model):
	course_code = models.CharField(max_length=6)
	course_name = models.CharField(max_length=40)

	def __str__(self):
		return self.course_name + '(' + self.course_code + ')'

class Assignment(models.Model):
	assignment_name = models.CharField(max_length=50, verbose_name = "Exam/Assignment")
	description = models.CharField(max_length=300, blank = True)
	pub_date = models.DateTimeField('date published')
	deadline = models.DateTimeField('deadline',null=False)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

	def __str__(self):
		return self.assignment_name

class Feedback(models.Model):
	fb_name = models.CharField(max_length=100, verbose_name='Feedback Name')
	pub_date = models.DateTimeField('date published')
	deadline = models.DateTimeField('deadline',null=False)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	class Meta:
		verbose_name = "Feedback"
		verbose_name_plural = "Feedbacks"

	def __str__(self):
		return self.fb_name


class Question(models.Model):
	question_text = models.CharField(max_length=300, null=False)
	feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
	class Meta:
		verbose_name = "Question"
		verbose_name_plural = "Questions"

	def __str__(self):
		return self.question_text

class Answer(models.Model):
	answer = models.CharField(max_length=500)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	def __str__(self):
		return self.answer

class Instructor(models.Model):
	course = models.ManyToManyField(Course, blank = True, default=1)
	user = models.OneToOneField(User)
	# __str__ for printing
	def __str__(self):
		return self.user.get_full_name()

class Student(models.Model):
	course = models.ManyToManyField(Course, blank = True, default=1)
	user = models.OneToOneField(User)
	# __str__ for printing
	def __str__(self):
		return self.user.get_full_name()
