from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractBaseUser, UserManager, BaseUserManager

# Create your models here.


class Course(models.Model):
	SPRING = 'SP'
	AUTUMN = 'AU'
	SUMMER = 'SU'

	SEMESTERS = (
		(SPRING, 'Spring'),
		(AUTUMN, 'Autumn'),
		(SUMMER, 'Summer'),
		)

	course_code = models.CharField(max_length=6, unique=True)
	course_name = models.CharField(max_length=40, blank=False)
	semester = models.CharField(
		max_length=2,
		choices=SEMESTERS,
		)
	def __str__(self):
		return self.course_name + '(' + self.course_code + ')'


class Assignment(models.Model):
	assignment_name = models.CharField(max_length=50, verbose_name = "Exam/Assignment")
	description = models.CharField(max_length=300, blank = True)
	pub_date = models.DateTimeField('date published')
	deadline = models.DateTimeField('deadline',null=False)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

	def is_past_deadline(self):
		return self.pub_date < timezone.now()

	def __str__(self):
		return self.assignment_name

class Feedback(models.Model):
	fb_name = models.CharField(max_length=100, verbose_name='Feedback Name')
	pub_date = models.DateTimeField('date published')
	deadline = models.DateTimeField('deadline',null=False, blank=False)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	class Meta:
		verbose_name = "Feedback"
		verbose_name_plural = "Feedbacks"

	def __str__(self):
		return self.fb_name


## Yes/No
## Multiple choice with one answer 
## Multiple choice with multiple answers answer 
## Comment area 
## Rating Scale
class Question(models.Model):
	TEXT_ANSWER = 'text'
	RATING = 'rate'

	TYPES = (
		(RATING, 'Rating Response'),
		(TEXT_ANSWER, 'Text Response'),
		)
	question_text = models.CharField(max_length=300, blank=False)
	feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
	question_type = models.CharField(max_length=4, choices=TYPES)

	class Meta:
		verbose_name = "Question"
		verbose_name_plural = "Questions"

	def __str__(self):
		return self.question_text

class Answer(models.Model):
	answer = models.CharField(max_length=500, blank=False)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	def __str__(self):
		return self.answer

class RatingAnswer(models.Model):
	question = models.OneToOneField(Question)
	responses1 = models.PositiveIntegerField()
	responses2 = models.PositiveIntegerField()
	responses3 = models.PositiveIntegerField()
	responses4 = models.PositiveIntegerField()
	responses5 = models.PositiveIntegerField()
	def __str__(self) :
		return 'Answer to ' + self.question.__str__()
	def count(self):
		return self.responses1 + self.responses2 + self.responses3 + self.responses4 + self.responses5

class Instructor(models.Model):
	course = models.ManyToManyField(Course, blank = True, default=1)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# __str__ for printing
	def __str__(self):
		return self.user.get_full_name()

class Student(models.Model):
	course = models.ManyToManyField(Course, blank = True, default=1)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	roll_no = models.CharField(max_length=11)
	# __str__ for printing
	def __str__(self):
		return self.user.get_full_name()
