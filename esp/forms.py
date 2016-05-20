from django import forms

from .models import PWM

class PWMForm(forms.ModelForm):
	class Meta:
		model = PWM
		fields = ('setting', 'on',)
