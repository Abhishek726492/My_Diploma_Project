from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from SmartSeating.models import RoomDetails
from SmartSeating.models import InvigilatorDetails
from django.contrib.auth.models import User
from SmartSeating.models import StudentCompleteDetails
from SmartSeating.models import StudentDetails
from django.db.models import Count
from django.db import models
from django.urls import reverse
from django.http import HttpResponse
import pandas as pd
from django.core.mail import EmailMessage
import random
from itertools import zip_longest
from datetime import datetime,timedelta
from .tasks import invigilators_email_to_admin
from .tasks import students_email_to_admin
from .tasks import mail_to_each_student
from .tasks import mail_to_each_invigilator
import pytz
# Create your views here.

all_students_pins=[]
selected_rooms_details=[]
m=6 
rd=None
all_data=[]
exam_date=None
exam_time=None
time_str=None
@csrf_exempt
def home(request):
  return render(request,'Home-page.html')

@csrf_exempt
def register(request):
  if request.method == 'POST':
    email = request.POST['email']
    user_name = request.POST['username']
    password = request.POST['password']
    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email already taken')
        return render(request, 'SignUp-Page.html')
    elif User.objects.filter(username=user_name).exists():
        messages.error(request, 'Username already exists')
        return render(request, 'SignUp-Page.html')
    else:
        # Create a new user
        user = User.objects.create_user(username=user_name, password=password, email=email)
        user.save()
        messages.success(request, 'Registration successful! Please login.')
        return render(request, 'Login-Page.html')
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
      messages.success(request,'Login Successfull!')
      return render(request,'Home-page.html')
    else:
      messages.error(request,'<span style="color:red; font-size:24px">&#9888;</span> Invalid data')
      return render(request,'Login-Page.html')
  else:
    return render(request,'Login-Page.html')
  

def examschedule(request):
   return render(request,'ExamSchedule-page.html')

  
def rooms(request):
  rooms = RoomDetails.objects.filter(user=request.user)
  return render(request,'Rooms-page.html',{'rooms':rooms})

@csrf_exempt
def addRoom(request):
  if request.method=="POST":
    room_number=request.POST.get('room-number')
    room_floor=request.POST.get('room-floor')
    room_rows=request.POST.get('room-rows')
    room_columns=request.POST.get('room-columns')
    existing_room = RoomDetails.objects.filter(
            user=request.user,
            room_no=room_number,
        ).exists()
    if not existing_room:
      RoomDetails.objects.create(
        user=request.user,
        room_no=room_number,
        rows=room_rows,
        cols=room_columns,
        room_floor=room_floor,
        room_capacity=int(room_rows)*int(room_columns)
      )
      rooms = RoomDetails.objects.filter(user=request.user)
      messages.success(request,f'Room {room_number} Added')
      return render(request,'Rooms-page.html',{'rooms':rooms})
    else:
      rooms = RoomDetails.objects.filter(user=request.user)
      messages.success(request,f'Room {room_number} already existed')
      return render(request,'Rooms-page.html',{'rooms':rooms})

@csrf_exempt
def removeRoom(request):
  if request.method=="POST":
    room_no=request.POST.get('room-number-2')
    existing_room = RoomDetails.objects.filter(
            user=request.user,
            room_no=room_no
        ).exists()
    if existing_room:
      room=get_object_or_404(RoomDetails, room_no=room_no,user=request.user)
      room.delete()
    else:
       messages.success(request,f'Room {room_no} not Available')
       rooms = RoomDetails.objects.filter(user=request.user)
       return render(request,'Rooms-page.html',{'rooms':rooms})
  rooms = RoomDetails.objects.filter(user=request.user)
  messages.success(request,f'Room {room_no} Removed')
  return render(request,'Rooms-page.html',{'rooms':rooms})

def invigilators(request):
  invigilators = InvigilatorDetails.objects.filter(user=request.user)
  return render(request,"Invigilators-page.html",{'invigilators':invigilators})

@csrf_exempt
def addInvigilator(request):
  if request.method=="POST":
    unique_number=request.POST.get('unique-number')
    name=request.POST.get('name')
    designation=request.POST.get('designation')
    email=request.POST.get('email')
    phone =  request.POST.get('phone')
    existing_invigilator = InvigilatorDetails.objects.filter(
            user=request.user,
            unique_no=unique_number
        ).exists()
    if not existing_invigilator:
      InvigilatorDetails.objects.create(
        user=request.user,
        unique_no=unique_number,
        name=name,
        designation=designation,
        email=email,
        phone=phone
      )
      invigilators = InvigilatorDetails.objects.filter(user=request.user)
      messages.success(request,f'Invigilator {unique_number}-{name} Added')
      return render(request,'Invigilators-page.html',{'invigilators':invigilators})
    else:
      invigilators = InvigilatorDetails.objects.filter(user=request.user)
      messages.success(request,f'Invigilator {unique_number} already existed')
      return render(request,'Invigilators-page.html',{'invigilators':invigilators})

@csrf_exempt
def removeInvigilator(request):
  if request.method=="POST":
    unique_no=request.POST.get('unique-number-2')
    existing_invigilator = InvigilatorDetails.objects.filter(
            user=request.user,
            unique_no=unique_no
        ).exists()
    if existing_invigilator:
      invigilator=get_object_or_404(InvigilatorDetails, unique_no=unique_no,user=request.user)
      invigilator.delete()
    else:
      messages.success(request,f'Invigilator {unique_no} not Available')
      invigilators = InvigilatorDetails.objects.filter(user=request.user)
      return render(request,'Invigilators-page.html',{'invigilators':invigilators})
  invigilators = InvigilatorDetails.objects.filter(user=request.user)
  messages.success(request,f'Invigilator {unique_no} Removed')
  return render(request,'Invigilators-page.html',{'invigilators':invigilators})


@csrf_exempt
def students(request):
    set_capacity(request)
    student_details = StudentDetails.objects.filter(user=request.user).order_by('id')
    return render(request, 'Students-page.html', {'students': student_details})

def set_capacity(request):
    # Fetch the student counts grouped by year and branch
    student_counts = StudentCompleteDetails.objects.filter(user=request.user).values('year', 'branch').annotate(count=models.Count('id'))

    # Reset capacity for all students under the current user
    StudentDetails.objects.filter(user=request.user).update(capacity=0)

    # Loop through student counts to update capacity
    for student_count in student_counts:
        year = student_count['year']
        branch = student_count['branch']
        count = student_count['count']

        # Update or create capacity for student with matching year and branch
        StudentDetails.objects.filter(user=request.user, year=year, branch=branch).update(capacity=count)

@csrf_exempt
def studentdetails(request):
  year=request.GET.get('year')
  branch=request.GET.get('branch')
  students = StudentCompleteDetails.objects.filter(user=request.user,year=year,branch=branch)
  return render(request,'StudentDetails-page.html',{'students':students,'year':year,'branch':branch})

@csrf_exempt
def addStudent(request):
  year = request.GET.get('year')
  branch = request.GET.get('branch')
  if request.method=="POST":
    name=request.POST.get('name')
    pin=request.POST.get('pin')
    email=request.POST.get('email')
    year=year
    branch=branch
    existing_student = StudentCompleteDetails.objects.filter(
            user=request.user,
            name=name,
            pin=pin,
            email=email,
            year=year,
            branch=branch
        ).exists()
    if not existing_student:
      StudentCompleteDetails.objects.create(
        user=request.user,
        name=name,
        pin=pin,
        email=email,
        year=year,
        branch=branch
      )
      # After adding a student, redirect to the student details page with updated parameters
      return render(request, 'StudentDetails-page.html', {
        'students': StudentCompleteDetails.objects.filter(user=request.user, year=year, branch=branch),
        'year': year,
        'branch': branch
      })
    # For GET requests, render the form with year and branch parameters
  return render(request, 'StudentDetails-page.html', {
      'students': StudentCompleteDetails.objects.filter(user=request.user, year=year, branch=branch),
      'year': year,
      'branch': branch
  })

@csrf_exempt
def removeStudent(request):
  year = request.GET.get('year')
  branch = request.GET.get('branch')
  if request.method=="POST":
    pin=request.POST.get('pin-2')
    existing_student = StudentCompleteDetails.objects.filter(
            user=request.user,
            pin=pin
        ).exists()
    if existing_student:
      student=get_object_or_404(StudentCompleteDetails, pin=pin,user=request.user)
      student.delete()
  # After adding a student, redirect to the student details page with updated parameters
      return render(request, 'StudentDetails-page.html', {
        'students': StudentCompleteDetails.objects.filter(user=request.user, year=year, branch=branch),
        'year': year,
        'branch': branch
      })

    # For GET requests, render the form with year and branch parameters
  return render(request, 'StudentDetails-page.html', {
      'students': StudentCompleteDetails.objects.filter(user=request.user, year=year, branch=branch),
      'year': year,
      'branch': branch
  })

@csrf_exempt
def allotment(request):
  global all_students_pins
  students = StudentDetails.objects.filter(user=request.user).order_by('id')
  total=0
  all_students_pins = []
  for s in students:
    total+=s.capacity
  return render(request, 'SeatAllotment-page1.html',{'students': students,'total': total})


@csrf_exempt
def selectRooms(request):
  global exam_date
  global exam_time
  global time_str
  if request.method=='POST':
    allrooms = RoomDetails.objects.filter(user=request.user).order_by('id')
    total=0
    for r in allrooms:
      total+=r.room_capacity
    selected_students=request.POST.get('selected_students')
    selected_branches=request.POST.getlist('branch_year')

    exam_date=request.POST.get('date')
    time_str=request.POST.get('time')
    actual_time=datetime.strptime(time_str,'%H:%M')
    new_time=actual_time - timedelta(minutes=25)
    exam_time=new_time.strftime('%H:%M')

    selected_student_details=StudentDetails.objects.filter(id__in=selected_branches)
    if not selected_branches:
      messages.success(request,'No Students selected')
      students = StudentDetails.objects.filter(user=request.user).order_by('id')
      total=0
      for s in students:
        total+=s.capacity
      return render(request, 'SeatAllotment-page1.html',{'students': students,'total': total})

        # Loop through each selected branch-year combination
    for s in selected_student_details:
      # Get all students for the current branch-year
      students_in_branch_year = StudentCompleteDetails.objects.filter(
          user=request.user,
          year=s.year,
          branch=s.branch
      ).values_list('pin', flat=True)  # Only retrieve the 'pin' field

      # Convert the QuerySet to a list and add it to the main list
      all_students_pins.append(list(students_in_branch_year))
    messages.success(request,f'{sum(len(sublist) for sublist in all_students_pins)} Students selected')

    required_seats=0
    summed = []
    lengths = [len(sublist) for sublist in all_students_pins]
    # if len(all_students_pins)<=6:
    #   required_seats = max(lengths)*6
    # else:
    batches = []
    for i in range(0,len(lengths),6):
      batches.append(lengths[i:i+6])
    transposed = zip_longest(*batches,fillvalue=0)
    summed = [sum(group) for group in transposed]
    required_seats = max(summed)*6
          
    return render(request,'SeatAllotment-page2.html',{'rooms':allrooms,'total': total,'all_students': all_students_pins,'students':required_seats})
  else:
    return HttpResponse('Invalid Request', status=400)
  

@csrf_exempt
def generateLayout(request):
  global selected_rooms_details
  if request.method=='POST':
    selected_rooms=request.POST.getlist('all_rooms')
    selected_rooms_details=RoomDetails.objects.filter(id__in=selected_rooms)
    if not selected_rooms:
       return HttpResponse('No rooms selected.', status=400)
    if not all_students_pins:
        return HttpResponse('No students selected.', status=400)
    
    branchList = all_students_pins[0:6]
    branchPointer = {f'branch{i+1}p': 0 for i in range(len(branchList))}

    # Room dimensions
    rows = 6
    cols = []
    for r in selected_rooms_details:
       cols.append(r.cols)

    # Number of rooms
    num_rooms = len(selected_rooms_details)

    # Create multiple rooms
    rooms = [[[None for _ in range(cols[room_index])] for _ in range(rows)] for room_index in range(num_rooms)]

    # Function to get branch pointer
    def returnPointer(index):
        return f'branch{index+1}p'

    # Function to get branch list
    def returnBranch(index):
        return branchList[index]


    def swap():
        global m
        for i in range(len(branchList)):
            branch = branchList[i]
            pointer = returnPointer(i)

            # Check if the current pointer has exhausted the branch
            if branchPointer[pointer] == len(branch):
                if m < len(all_students_pins):
                    branchList[i] = all_students_pins[m]  # Swap the exhausted branch with a new one
                    branchPointer[pointer] = 0  # Reset the pointer for the new branch
                    m += 1  # Move to the next branch in all_students_pins


    def fill_room(room, room_index, cols):
        x = 0
        n = k = 1
        for i in range(rows):
            for j in range(1):
                n = k = 1
                room[i][j] = x
                while n < cols:
                    room[(i + n + k) % rows][j + n] = x
                    n += 1
                    k += 1
                x += 1

        # Replace numbers with values from lists
        for i in range(rows):
            for j in range(cols):
                branch_index = room[i][j]
                if branch_index is not None and 0 <= branch_index < len(branchList):
                    pointer_key = returnPointer(branch_index)
                    branch = returnBranch(branch_index)
                    if branchPointer[pointer_key] < len(branch):
                        room[i][j] = branch[branchPointer[pointer_key]]
                        branchPointer[pointer_key] += 1
                    else:
                        room[i][j] = '-'
                else:
                    room[i][j] = '-'
                swap()
    a=1
    # Fill all rooms
    for room_index, room in enumerate(rooms):
        fill_room(room, room_index, cols[room_index])

    #convert to excel sheets
    for room,r in zip(rooms, selected_rooms_details):
      pf=pd.DataFrame(room)
      pf.to_excel(f'{request.user.username}_Room{r.room_no}.xlsx',index=False,engine='openpyxl')
      a+=1

    # #sending mail of students allotment to admin via celery worker
    selected_rooms_list = list(selected_rooms_details.values("room_no", "room_capacity"))
    students_email_to_admin.delay(request.user.username, request.user.email, selected_rooms_list,exam_date,time_str)

    global rd
    global all_data
    all_data=[]
    seating_data=[]
    seat_number = 1  # Start numbering from 1

    for r in selected_rooms_details:
        seat_number=1
        file_path = rf'C:\Users\thoka\DjangoProjects\first\{request.user}_Room{r.room_no}.xlsx'
        rd = pd.read_excel(file_path, sheet_name='Sheet1')

        # Iterate through columns first (column-wise iteration)
        for col in rd.columns:
            for seat in rd[col]:
                if pd.notna(seat) and seat != "-":  # Only consider non-empty seats
                    # Assign seat number
                    seating_data.append({
                        'room': r.room_no,
                        'seat_id': seat_number,  # Column-wise seat number
                        'seat_value': seat  # This will be your seat assignment (e.g., 24001-CS-001)
                    })
                seat_number += 1
    invigilators = InvigilatorDetails.objects.filter(user=request.user)
    total = len(invigilators)
    messages.success(request,'Seating Allotment Generated!<br>It will be sent to your mail')

    # #calculate time
    examination_date = datetime.strptime(exam_date, '%Y-%m-%d').date()  # Convert to date object
    examination_time = datetime.strptime(time_str, '%H:%M').time()  # Convert to time object
    exam_datetime=datetime.combine(examination_date,examination_time)
    time_before_exam=exam_datetime-timedelta(minutes=25)
    timezone=pytz.timezone('Asia/Kolkata')
    email_send_time=timezone.localize(time_before_exam)

    #sending mails to students before 25 mins of exam
    for i in range(0,len(seating_data)):
       pin_number=seating_data[i]['seat_value']
       room_number=seating_data[i]['room']
       seat_no=seating_data[i]['seat_id']
       to_mail = StudentCompleteDetails.objects.get(user=request.user,pin=pin_number).email
       name = StudentCompleteDetails.objects.get(user=request.user,pin=pin_number).name
       mail_to_each_student.apply_async(
          args= (exam_date,time_str,pin_number,name,room_number,seat_no,to_mail,),
          eta=email_send_time
       )

  return render(request,'SeatAllotment-page3.html',{'invigilators':invigilators, 'total': total,'selected_rooms':len(selected_rooms),'seating': seating_data})


@csrf_exempt
def assignInvigilators(request):
  invigilators_assign = []

  if request.method == 'POST':
      selected_invigilators = request.POST.getlist('all_invigilators')
      selected_invigilators_details = list(InvigilatorDetails.objects.filter(unique_no__in=selected_invigilators))

      # Randomize the order of invigilators
      random.shuffle(selected_invigilators_details)

      # Step 1: Assign one invigilator to each room
      invigilator_index = 0
      for room in selected_rooms_details:
          if invigilator_index < len(selected_invigilators_details):
              invigilators_assign.append({
                  'room': room.room_no,
                  'invigilators': [{'invigilator': selected_invigilators_details[invigilator_index].unique_no,
                                   'name': selected_invigilators_details[invigilator_index].name
                  }],
                  'room_capacity':room.room_capacity
              })
              invigilator_index += 1

      # Step 2: Assign remaining invigilators to rooms with higher capacity (distributed)
      remaining_invigilators = selected_invigilators_details[invigilator_index:]  # Remaining invigilators after Step 1

      # Sort rooms by capacity in descending order to fill higher capacity rooms first
      rooms_sorted_by_capacity = sorted(invigilators_assign, key=lambda r: r['room_capacity'], reverse=True)

      # Distribute remaining invigilators in a round-robin fashion
      room_index = 0
      total_rooms = len(rooms_sorted_by_capacity)

      for invigilator in remaining_invigilators:
          # Cycle through rooms and add invigilators if capacity allows
          while len(rooms_sorted_by_capacity[room_index]['invigilators']) >= rooms_sorted_by_capacity[room_index]['room_capacity']:
              room_index = (room_index + 1) % total_rooms  # Move to the next room
          
          # Add invigilator to the current room
          rooms_sorted_by_capacity[room_index]['invigilators'].append({
              'invigilator': invigilator.unique_no,
              'name': invigilator.name
          })

          # Move to the next room (round-robin distribution)
          room_index = (room_index + 1) % total_rooms
  for assignment in invigilators_assign:
    assignment.pop('room_capacity', None)
  mail=request.user.email
  local, domain = mail.split('@')
  if len(mail)<=5:
     email=mail
  else:
     email=local[:3] + '*' * (len(local) - 5) + local[-2:] + '@' + domain
  messages.success(request,'Invigilators Assigned!<br>Everything DONE!')

  excel_data = []
  for assignment in invigilators_assign:
      invigilator_details = ', '.join([f"{invigilator['name']} ({invigilator['invigilator']})" 
                                        for invigilator in assignment['invigilators']])
      excel_data.append({
          'Room': assignment['room'],
          'Invigilators': invigilator_details  # All invigilators for that room as a single string
      })

  #mailing invigilator details to admin

  dfi = pd.DataFrame(excel_data)
  dfi.to_excel(f'{request.user.username}_Invigilators_Details.xlsx',index=False,engine='openpyxl')

  # #sending invigilators details to admin via celery worker
  invigilators_email_to_admin.delay(request.user.username,request.user.email,exam_date,time_str)

  #calculate time
  examination_date = datetime.strptime(exam_date, '%Y-%m-%d').date()  # Convert to date object
  examination_time = datetime.strptime(time_str, '%H:%M').time()  # Convert to time object
  exam_datetime=datetime.combine(examination_date,examination_time)
  time_before_exam=exam_datetime-timedelta(minutes=25)
  timezone=pytz.timezone('Asia/Kolkata')
  email_send_time=timezone.localize(time_before_exam)
  #sending mail to all invigilators
  for i in range(0,len(invigilators_assign)):
      for j in range(0,len(invigilators_assign[i]['invigilators'])):
        unique_no = invigilators_assign[i]['invigilators'][j]['invigilator']
        to_email=InvigilatorDetails.objects.get(user=request.user,unique_no=unique_no).email
        room=invigilators_assign[i]['room']
        name=invigilators_assign[i]['invigilators'][j]['name']
        mail_to_each_invigilator.apply_async(
           args=(exam_date,time_str,unique_no,to_email,room,name,),
           eta=email_send_time
        )

  return render(request, 'SeatAllotment-page4.html', {'email': email,'date':exam_date,'time':exam_time,'invigilators':invigilators_assign})


@csrf_exempt
def logout(request):
  auth.logout(request)
  return redirect('/')