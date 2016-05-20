from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.apps import apps
from .models import PWM, Device


class IndexView(generic.ListView):
    model = PWM
    template_name = 'esp/index.html'
    def get_queryset(self):
	return PWM.objects.all()

class PWMControl(generic.edit.UpdateView):
    model = PWM
    fields =['setting', 'on']
    template_name = 'esp/control.html'

def submit(request, pwm_id):
    pwm = get_object_or_404(PWM, pk=pwm_id)
    if 'on' in request.POST.keys():
	on = True
    else:
	on = False
    pwm.set(request.POST['setting'], on)
    return redirect('esp:control',pk=pwm_id)
