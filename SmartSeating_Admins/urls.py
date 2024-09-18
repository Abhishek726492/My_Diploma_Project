from django.urls import path
from . import views
urlpatterns=[
  path('home',views.home,name='home'),
  path('register',views.register,name='register'),
  path('login',views.login,name='login'),
  path('examschedule',views.examschedule,name='examschedule'),
  path('logout',views.logout,name='logout'),
  path('rooms',views.rooms,name='rooms'),
  path('students',views.students,name='students'),
  path('studentdetails',views.studentdetails,name='studentdetails'),
  path('addRoom',views.addRoom,name="addRoom"),
  path('removeRoom',views.removeRoom,name="removeRoom"),
  path('invigilators',views.invigilators,name='invigilators'),
  path('addInvigilator',views.addInvigilator,name="addInvigilator"),
  path('removeInvigilator',views.removeInvigilator,name="removeInvigilator"),
  path('addStudent',views.addStudent,name='addStudent'),
  path('removeStudent',views.removeStudent,name='removeStudent'),
  path('allotment',views.allotment,name='allotment'),
  path('selectRooms',views.selectRooms,name='selectRooms'),
  path('generateLayout',views.generateLayout,name='generateLayout'),
  path('assignInvigilators',views.assignInvigilators,name='assignInvigilators')
]