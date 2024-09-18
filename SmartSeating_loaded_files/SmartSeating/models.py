from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RoomDetails(models.Model):
  room_no = models.IntegerField()
  rows = models.IntegerField()
  cols = models.IntegerField()
  room_floor = models.IntegerField()
  room_capacity = models.IntegerField()