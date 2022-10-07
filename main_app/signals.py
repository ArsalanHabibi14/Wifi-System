from .models import Wifi, Connections
from django.db.models.signals import pre_save, post_save

def create_name(sender, instance, **kwargs):
	if not instance.wifi_name:
		instance.wifi_name = f"{instance.owner.username}-WF"

pre_save.connect(create_name, Wifi)

def end_connection(sender, instance, **kwargs):
	wifi = instance
	if wifi.is_active == False:
		connection = Connections.objects.filter(wifis=wifi)
		for s in connection:
			s.is_connect = False
			s.save() 

post_save.connect(end_connection, Wifi)

def start_connection(sender, instance, **kwargs):
	wifi = instance
	if wifi.is_active == True:
		connection = Connections.objects.filter(wifis=wifi)
		for s in connection:
			s.is_connect = True
			s.save() 

post_save.connect(start_connection, Wifi)