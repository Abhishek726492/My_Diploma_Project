from django.urls import path
from . import views
from SmartSeating_Admins import views

urlpatterns = [
  path('',views.home,name='home')
]