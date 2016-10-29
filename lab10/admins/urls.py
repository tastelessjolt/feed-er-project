from django.conf.urls import url, include

from . import views

app_name = 'admins'
urlpatterns = [
	url(r'^$', views.LoginView, name='login'),
	url(r'^login/$', views.LoginView, name='log_in'),
	url(r'^index/$', views.IndexView, name='index'),
	url(r'^logout/$', views.Logout, name='logout'),
]