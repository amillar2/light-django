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
	def save_model(self, request, obj, form, change):
	    if not obj.pk: # call super method if object has no primary key 
		super(DeviceAdmin, self).save_model(request, obj, form, change)
	    else:
		pass # don't actually save the parent instance

	def save_related(self, request, form, formsets, change):
	    form.save_m2m()
	    for formset in formsets:
		self.save_formset(request, form, formset, change=change)
	    super(DeviceAdmin, self).save_model(request, form.instance, form, change)

class SwitchAdmin(admin.ModelAdmin):
	model = Switch
	filter_horizontal = ('pwm',)
        fields = ['pwm']
	list_display = ('pretty_name','room')

admin.site.register(Device, DeviceAdmin)
admin.site.register(Switch, SwitchAdmin)

