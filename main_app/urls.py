from django.urls import path
from . import views


urlpatterns = [
	path("", views.HomePageView.as_view(), name='home_page'),
	path('login/', views.LoginPage.as_view(), name='login_page'),
	path('register/', views.register_page, name='register_page'),
	path('connect/<int:pk>/password/', views.password_connection, name='password_connection'),
	path('file/', views.history_page, name='files_page'),
	path("send/", views.send_file_page, name='send_file_page'),
	path("active/", views.active_wifi, name="active")
]