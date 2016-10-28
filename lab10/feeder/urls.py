from django.conf.urls import url

from . import views

app_name = 'feeder'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^register/$', views.RegisterView.as_view(), name='register'),
	url(r'^login/$', views.IndexView.as_view(), name='login'),
	url(r'^AddSession/$', views.AddSession, name='session'),
]