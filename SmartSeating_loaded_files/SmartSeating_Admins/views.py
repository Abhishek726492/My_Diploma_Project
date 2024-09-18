from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def register(request):
  if request.method == 'POST':
    email = request.POST['email']
    user_name = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username=user_name,password=password,email=email)
    user.save()
    return render(request,'Login-Page.html')
  else:
    return render(request,'SignUp-Page.html')
  
@csrf_exempt
def login(request):
  if request.method == 'POST':
    user_name = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=user_name,password=password)

    if user is not None:
      auth.login(request, user)
      return render(request,'Home-page.html')
    else:
      messages.info(request,'Invalid data')
  else:
    return render(request,'Login-Page.html')
  
@csrf_exempt
def logout(request):
  auth.logout(request)
  return redirect('/')