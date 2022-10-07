from .models import Wifi, Connections
import os


def get_wifis(username):
	get_wifi = Wifi.objects.filter(owner__username__iexact=username).first()
	return get_wifi

def connection_func(wifi):
	user_list = []
	connection  = Connections.objects.filter(wifis__wifi_name=wifi.wifi_name, is_connect=True)
	for s in connection:
		user_list.append(s.user)
	return user_list

def get_file_name(file):
	basename = os.path.basename(str(file))
	name, ext = os.path.splitext(str(file))
	return f"{name}{ext}"