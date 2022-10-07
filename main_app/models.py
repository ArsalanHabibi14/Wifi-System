from django.db import models
from django.contrib.auth.models import User
import uuid

class Wifi(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
	wifi_name = models.CharField(max_length=200, null=True, blank=True)
	wifi_password = models.CharField(max_length=200)
	created = models.DateTimeField(max_length=120)
	is_active = models.BooleanField(default=False)

	def __str__(self):
		return self.wifi_name

class Connections(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	wifis = models.ForeignKey(Wifi, on_delete=models.CASCADE)
	is_connect = models.BooleanField(default=False)

	def __str__(self):
		if self.is_connect:
			return f"{self.user.username} Connected to The {self.wifis.wifi_name} Wifi"
		else:
			return f"{self.user.username} Not Connected to the {self.wifis.wifi_name} Wifi"

class Files(models.Model):
	admin_wifi = models.ForeignKey(Wifi, on_delete=models.CASCADE, null=True)
	file = models.FileField(upload_to="files/")
	receivers = models.ManyToManyField(User, related_name="receivers")
	send_time = models.DateTimeField(auto_now_add=True)
	id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

	def __str__(self):
		return self.admin_wifi.wifi_name