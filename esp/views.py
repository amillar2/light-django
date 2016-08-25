from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.apps import apps
from .models import PWM, Device
import json

class IndexView(generic.ListView):
    model = PWM
    template_name = 'esp/index.html'
    def get_queryset(self):
	return PWM.objects.all()

class PWMControl(generic.edit.UpdateView):
    model = PWM
    fields =['setting', 'on']
    template_name = 'esp/control.html'


def submit(request):
    if request.method == 'POST':
        pwm_id = request.POST.get('pwm_id')
	pwm = PWM.objects.filter(pk=pwm_id)
	if pwm:
		pwm = pwm[0]
		if 'on' in request.POST.keys():
			if(request.POST.get('on')=='true'):
				on = True
			elif(request.POST.get('on')=='false'):
				on = False
		else:
			on = True
		if 'setting' in request.POST.keys():
			setting = int(request.POST.get('setting'))
		else:
			setting = pwm.setting
		pwm.set(setting*255/100,on)
		response_data = {'result':'success'}
	else:
		response_data = {'result':'no such pwm'}
	

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

def toggle(request):
    if request.method == 'POST':
        pwm_id = request.POST.get('pwm_id')
	pwm = PWM.objects.filter(pk=pwm_id)
	if pwm:
		pwm[0].toggle()
		response_data = {'result':'success'}
	else:
		response_data = {'result':'no such pwm'}
	

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

def update(request):
    if request.method == 'GET':
        pwm_id = request.GET.get('pwm_id')	
        response_data = {}
	pwm = PWM.objects.filter(pk=pwm_id)
	if pwm:
		pwm = pwm[0]
		response_data = {'setting':pwm.setting, 'on':pwm.status() }
	else:
		response_data = {'result':'no such pwm'}

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

