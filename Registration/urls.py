from django.urls import path
from . import views

app_name = 'Registration'

urlpatterns = [
    path('registration', views.registration , name='registration'),
    path('login', views.user_login , name='user_login'),
    path('LoggedOut', views.Logout, name="Logout"),
    ]