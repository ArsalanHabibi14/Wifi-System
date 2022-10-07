from django.views import View
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, FileForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Wifi, Connections, Files
import httpagentparser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .utils import get_wifis, connection_func, get_file_name
from django.contrib import messages

class HomePageView(View):
	def get(self, request):
		if request.user.is_authenticated:
			connections = Connections.objects.filter(user=request.user, is_connect=True)
			if connections.exists():
				return redirect("files_page")
		get_user = User.objects.filter(username=request.user.username).first()
		agent = request.META['HTTP_USER_AGENT']
		s = httpagentparser.detect(agent)
		wifis = Wifi.objects.filter(is_active=True)
		context = {
			'wifis' : wifis,
			'system' : s
		}
		return render(request, 'wifi/home.html', context)

class LoginPage(LoginView):
	template_name = "account/login.html"


def register_page(request):
	form = CustomUserCreationForm()
	context = {
		'form' : form
	}
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			login(request, user)
			return redirect('/')
	return render(request, 'account/register.html', context)

def history_page(request):
	connection = Connections.objects.filter(user=request.user, is_connect=True).first()
	context = {}
	file_list = []
	if connection is not None:
		get_wifi = connection.wifis
		get_files = Files.objects.filter(admin_wifi=get_wifi, receivers=request.user)
		for c in get_files:
			file_name = get_file_name(c.file)
			file_list.append(file_name)
		context['files'] = file_list
	return render(request, "wifi/wifi_files.html", context)

@login_required(login_url="/login/")
def password_connection(request, pk):
	get_wifi = Wifi.objects.filter(id=pk).first()
	
	context = {}
	if request.method == "POST":
		password = request.POST.get('password')
		if str(get_wifi.wifi_password) == str(password):
			get_connection = Connections.objects.filter(user=request.user, wifis=get_wifi).first()
			if get_connection is None:
				Connections.objects.create(user=request.user, wifis=get_wifi, is_connect=True)
			else:
				get_connection.is_connect = True
				get_connection.save()
			return redirect('/')
	return render(request, 'wifi/connection_password.html', context)

def send_file_page(request):
	login_user_wifi = get_wifis(request.user.username)
	if not login_user_wifi.is_active:
		return redirect("/")
	form = FileForm()
	wifi = get_wifis(request.user.username)
	connections = connection_func(wifi)
	context = {
		'form' : form,
		'connections' : connections
	}
	wifi = get_wifis(request.user.username)
	connections = connection_func(wifi)
	if request.method == "POST":
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			data = form.save(commit=False)
			data.admin_wifi = wifi
			data.save()
			get_id = data.id
			file = Files.objects.filter(id=get_id).first()
			for s in connections:
				file.receivers.add(s)
				file.save()
			return redirect("files_page")
	return render(request, 'wifi/send_file.html', context)


def active_wifi(request):
	wifi = Wifi.objects.filter(owner=request.user, is_active=False).first()
	if request.user.is_authenticated:
		if wifi is not None:
			wifi.is_active = True
			wifi.save()
			messages.success(request, "Successfully wifi actived")
		else:
			messages.error(request, "Your wifi already actived")
	return redirect('/')