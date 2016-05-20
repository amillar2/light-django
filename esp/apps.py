from __future__ import unicode_literals

from django.apps import AppConfig

class EspConfig(AppConfig):
    name = 'esp'
    verbose_name = 'Lighting Control'
    def ready (self):
	from .mqtt_init import mqtt_init
	print 'Starting MQTT client...'
	self.client = mqtt_init()
