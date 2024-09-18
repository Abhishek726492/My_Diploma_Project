from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.

def home(request):
  return render(request,'Home-page.html')