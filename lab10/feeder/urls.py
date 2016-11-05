from django.conf.urls import url, include
# from django.contrib.auth import views as auth_views

from . import views

app_name = 'feeder'
urlpatterns = [
	url(r'^$', views.LoginView, name='login'),
	url(r'^login/$', views.LoginView, name='log_in'),
	url(r'^register/$', views.RegisterView, name='register'),
	url(r'^index/$', views.IndexView, name='index'),
	url(r'^logout/$', views.Logout, name='logout'),
	url(r'^tokensignin/$', views.TokenVerify, name='gtoken'),
	url(r'^studentlogin/$', views.StudentLogin, name='studentlogin'),

]