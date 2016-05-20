from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.apps import apps
import json
# Create your models here.

@python_2_unicode_compatible
class Device(models.Model):
    espID = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    online = models.BooleanField(default=False)
    def status(self):
	return 'Online' if self.online else 'Offline'
    def get_absolute_url(self):
        return reverse('esp:config', args=(self.pk,))
    def save(self, *args, **kwargs):
	print('saving device')
        super(Device, self).save(*args, **kwargs)
	self.config_device()
    def config_device(self):
	config = {}
	i=1
	print('sending config message')
	for pwm in self.pwm_set.all():
		config['mqtt_topic_pwm%d'%i] = pwm.topic
		i+=1
	i=1
        for sw in self.switch_set.all():
                config['mqtt_topic_sw%d'%i] = sw.topic
		i+=1
	client = apps.get_app_config('esp').client
    	client.publish(topic=self.espID,payload=json.dumps(config), qos=2, retain=False)

    def update_status(self, statusData):
	#set online status
	if 'online' in statusData.keys():
		self.online = statusData['online']
	#loop through device pwms, update status, and save
	for pwm in self.pwm_set.all():
		if pwm.topic in statusData.keys():
			pwm.setting = statusData[pwm.topic]['setting']
			pwm.on = statusData[pwm.topic]['on']
			pwm.save()
	#loop through device switches, update state, and save
	for sw in self.switch_set.all():
		if sw.topic in statusData.keys():
			sw.on = statusData[sw.topic]
			sw.save()
    def __str__(self):
	return self.name

@python_2_unicode_compatible
class PWM(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    room = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    pretty_name = models.CharField(max_length=200, default='')
    setting = models.IntegerField(default=0)
    on = models.BooleanField(default=False)
    channel = models.IntegerField(default=0)
    def status(self):
	return 'On' if self.on else 'Off'
    def set(self, setting, on):
	print('setting pwm:' + self.pretty_name)
	cmdOut = {}
	cmdOut['deviceOn'] = on
	cmdOut['deviceSetting'] = setting
	client = apps.get_app_config('esp').client
	client.publish(topic=self.topic,payload=json.dumps(cmdOut),qos=2,retain=True)
    def toggle(self):
	self.set(self.setting,not(self.on))
    def save(self, *args, **kwargs):
        self.topic = self.room + '/' + self.name
        if self.pretty_name == '':
		self.pretty_name = self.name
        super(PWM, self).save(*args, **kwargs)
    def get_absolute_url(self):
	return reverse('esp:control', args=(self.pk,))
#add function for publish
    def __str__(self):
	return self.pretty_name

@python_2_unicode_compatible
class Switch(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    pwm = models.ManyToManyField(PWM)
    room = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    pretty_name = models.CharField(max_length=200, default='')
    on = models.BooleanField(default=False)
    channel = models.IntegerField(default=0)
    def toggle_pwm(self):
	print('toggling pwms for switch' + self.pretty_name)
	for pwm in self.pwm.all():
		pwm.toggle()
    def save(self, *args, **kwargs):
	self.topic = self.room + '/switch/' + self.name
	if self.pretty_name == '':
		self.pretty_name = self.name 
        super(Switch, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

