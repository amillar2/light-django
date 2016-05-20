from django.conf.urls import url

from . import views

app_name = 'esp'

urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^(?P<pk>[0-9]+)/$', views.PWMControl.as_view(), name='control'),
	url(r'^(?P<pwm_id>[0-9]+)/submit/$', views.submit, name='submitControl'),
	]

