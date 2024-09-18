from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RoomDetails(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  room_no = models.IntegerField()
  rows = models.IntegerField()
  cols = models.IntegerField()
  room_floor = models.IntegerField()
  room_capacity = models.IntegerField()

class InvigilatorDetails(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  unique_no = models.IntegerField(primary_key=True)
  name =  models.CharField(max_length=100)
  designation = models.CharField(max_length=200)
  email = models.EmailField(max_length=254)
  phone = models.BigIntegerField()

class StudentDetails(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  year = models.CharField(max_length=10)
  branch = models.CharField(max_length=10)
  capacity = models.IntegerField()

class StudentCompleteDetails(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=200)
  pin = models.CharField(max_length=20)
  year = models.CharField(max_length=10)
  branch = models.CharField(max_length=10)
  email = models.EmailField(max_length=254)