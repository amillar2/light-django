from django.contrib import admin

from .models import Device, PWM, Switch

class PWMInline(admin.StackedInline):
	model = PWM
	extra = 2
	max_num = 2
	fields = ['name','pretty_name', 'room', 'topic']
	readonly_fields = ('topic',)

class SwitchInline(admin.StackedInline):
	model = Switch
	extra = 2
	max_num = 2
	fields = ['name', 'pretty_name', 'room', 'topic', 'on']
	readonly_fields = ('topic', 'on',)

class DeviceAdmin(admin.ModelAdmin):
	list_display = ('name', 'espID', 'status')
	fields = ['espID','name', 'online']
	readonly_fields = ('online',)
    	inlines = [PWMInline,SwitchInline]

class SwitchAdmin(admin.ModelAdmin):
	model = Switch
	filter_horizontal = ('pwm',)
        fields = ['pwm']

admin.site.register(Device, DeviceAdmin)
admin.site.register(Switch, SwitchAdmin)

