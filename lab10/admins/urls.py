from django.conf.urls import url, include

from . import views

app_name = 'admins'
urlpatterns = [
	url(r'^$', views.LoginView, name='login'),
	url(r'^login/$', views.LoginView, name='log_in'),
	url(r'^index/$', views.IndexView, name='index'),
	url(r'^logout/$', views.Logout, name='logout'),
	url(r'^addcourse/$', views.AddCourse, name='addcourse'),
	url(r'^courses/$', views.AllCourses, name='courses'),
	url(r'^courses/(?P<pk>[0-9]+)/$', views.GetCourse, name='course'),
	url(r'^instructors/$', views.AllInstructors, name='instructors'),
	url(r'^instructors/(?P<pk>[0-9]+)/$', views.GetInstructor, name='instructor'),
]