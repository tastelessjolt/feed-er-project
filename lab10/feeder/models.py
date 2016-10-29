from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, UserManager, BaseUserManager

# Create your models here.


# class MyUser(AbstractBaseUser):
# 	identifier = models.EmailField(unique=True)
# 	first_name = models.CharField(max_length=30,null=True)
# 	last_name = models.CharField(max_length=30,null=True)
# 	# email = models.EmailField('E-mail')
# 	objects = UserManager()
# 	REQUIRED_FIELDS = ['first_name','last_name','EmailField']
# 	USERNAME_FIELD = 'identifier'

class Course(models.Model):
	course_code = models.CharField(max_length=6)
	course_name = models.CharField(max_length=40)

	def __str__(self):
		return self.course_name + '(' + self.course_code + ')'

class Assignment(models.Model):
	assignment_name = models.CharField(max_length=50)
	description = models.CharField(max_length=300, blank = True)
	pub_date = models.DateTimeField('date published')
	deadline = models.DateTimeField('deadline')
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

	def __str__(self):
		return self.assignment_name

class Instructor(models.Model):
	# first_name = models.CharField(max_length=30)
	# last_name = models.CharField(max_length=30)
	# email = models.EmailField('E-mail')
	course = models.ManyToManyField(Course, blank = True, default=1)
	user = models.OneToOneField(User)
	# __str__ for printing
	def __str__(self):
		return self.user.get_full_name()

class Student(models.Model):
	# first_name = models.CharField(max_length=30)
	# last_name = models.CharField(max_length=30) 
	# email = models.EmailField()
	course = models.ManyToManyField(Course, blank = True, default=1)
	user = models.OneToOneField(User)

	# __str__ for printing
	def __str__(self):
		return self.user.get_full_name()
