from django.conf.urls import url

from . import views

app_name = 'feeder'
urlpatterns = [
	url(r'^(?P<pk>[0-9]+)/$', views.IndexView.as_view(), name='index'),
	url(r'^register/$', views.RegisterView.as_view(), name='register'),
	url(r'^login/$', views.RegisterView.as_view(), name='login'),
	url(r'^index/$', views.RegisterView.as_view(), name='login'),

	# url(r'^/$', )
	# url(r'^(?P<pk>[0-9]+)/$',views.vote, name='vote'),
]