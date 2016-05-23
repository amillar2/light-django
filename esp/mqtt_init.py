import paho.mqtt.client as mqtt
import json
from .models import Switch, Device, PWM 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	#subscribe to status and discovery topics    
    	client.subscribe("+/status")
	client.subscribe("discovery")
	#subscribe to switch topics
	client.subscribe("+/switch/#")
# The callback for when a PUBLISH message is received from the server.
"""
def on_message(client, userdata, msg):
    	print(msg.topic+": "+str(msg.payload))
	if "status" in msg.topic:
		print("Received status message on " + msg.topic + " : " + msg.payload)
	if "discovery" in msg.topic:
		print("Received discovery message: " + msg.payload)
def on_publish(client, userdata, mid):
	print("Published message")
"""

def on_status(client, userdata, msg):
	#grab espID from <espID>/status topic string
	espID = msg.topic.split('/')[0]
	print(msg.payload) 
	if msg.payload:
		statusData = json.loads(msg.payload)
		d = Device.objects.filter(espID=espID)
		#if device exists, update status
		if d:
			d = d[0]
			d.update_status(statusData)
		else:
			print("Received status from unknown device")
	

def on_discovery(client, userdata, msg):
	print('received discovery messgage')
	#get espID
	espID = msg.payload
	#if espID exists, configure
	d = Device.objects.filter(espID=espID)
	if d:
		d[0].config_device()
	#if espID does not exist, make new object and save
	else:
		Device.objects.create(espID=espID, name=espID)

def on_switch(client, userdata, msg):
	print("received switch input")
	sw = Switch.objects.filter(topic=msg.topic)
	#if switch exists, toggle pwms
	print(sw)
	if sw:
		sw[0].toggle_pwm()
	
def mqtt_init():
	client = mqtt.Client()
	client.on_connect = on_connect
	#client.on_message = on_message #for test/debug. uncomment func defs if used
	#client.on_publish = on_publish
	#add topic callbacks here
	client.message_callback_add("+/status", on_status)
	client.message_callback_add("discovery", on_discovery)
	client.message_callback_add("+/switch/#", on_switch)
	client.username_pw_set('test', password='testpass')
	client.connect("localhost",port=1883, keepalive=60)
	client.loop_start()
	return client
