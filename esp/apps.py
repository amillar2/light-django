from __future__ import unicode_literals

from django.apps import AppConfig

class EspConfig(AppConfig):
    name = 'esp'
    verbose_name = 'Lighting Control'
    def ready (self):
	from .mqtt_init import mqtt_init
	from .models import alexa_discovery 
	print 'Starting MQTT client...'
	self.client = mqtt_init()
	alexa_discovery(self.client)
