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
	url(r'^addfeedback/$', views.AddFeedback, name='addfeedback'),
	url(r'^feedbacks/$', views.AllFeedbacks, name='feedbacks'),
	url(r'^feedbacks/(?P<pk>[0-9]+)/$', views.FeedbackView, name='feedback'),
	url(r'^adddeadline/$', views.AddAssignment, name='adddeadline'),
	url(r'^assignments/$', views.AllAssignments, name='assignments'),
	url(r'^assignments/(?P<pk>[0-9]+)/$', views.AssignmentView, name='assignment'),
	url(r'^apiendpoint/$', views.APIendpoint, name = 'apiendpoint')
]