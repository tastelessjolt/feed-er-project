from __future__ import unicode_literals

from django.db import models

# Create your models here.

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
	first_name = models.CharField(max_length=30)
	second_name = models.CharField(max_length=30)
	email = models.EmailField('E-mail')
	course = models.ManyToManyField(Course, blank = True)
	# __str__ for printing
	def __str__(self):
		return self.first_name + ' ' + self.second_name

class Student(models.Model):
	first_name = models.CharField(max_length=30)
	second_name = models.CharField(max_length=30) 
	email = models.EmailField()
	course = models.ManyToManyField(Course, blank = True)

	# __str__ for printing
	def __str__(self):
		return self.first_name + ' ' + self.second_name
