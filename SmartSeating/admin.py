from django.contrib import admin
from .models import RoomDetails
from .models import InvigilatorDetails
from .models import StudentDetails, StudentCompleteDetails
# Register your models here.
admin.site.register(RoomDetails)
admin.site.register(InvigilatorDetails)
admin.site.register(StudentDetails)
admin.site.register(StudentCompleteDetails)