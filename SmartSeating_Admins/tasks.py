#Mailing
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from SmartSeating.models import StudentCompleteDetails
from SmartSeating.models import InvigilatorDetails
import os
from datetime import datetime, timedelta
from first.settings import BASE_DIR

@shared_task(bind=True)
def students_email_to_admin(self,user_name,user_email,selected_rooms_list,exam_date,exam_time):
  try:
    email = EmailMessage(
       subject=f'Examination on {exam_date} at {exam_time} Seating Arrangement',
       body='Download the below attached excel files to view the seating plan',
       from_email=settings.EMAIL_HOST_USER,
       to=[user_email],
    )

    for r in selected_rooms_list:
       file_path = os.path.join(BASE_DIR,f'{user_name}_Room{r["room_no"]}.xlsx')
       with open(file_path,'rb') as f:
          excel_file=f.read()
          file_name=f'{user_name}_Room{r["room_no"]}.xlsx'
          email.attach(file_name,excel_file,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
    return 'Email Sent'
  
  except FileNotFoundError:
    return f'Files not found'
  except Exception as e:
    return f'Error: {str(e)}'

@shared_task(bind=True)
def invigilators_email_to_admin(self,user_name,user_email,exam_date,exam_time):
  try:
    email = EmailMessage(
        subject=f'Examination on {exam_date} at {exam_time} Seating Arrangement',
        body='Download the below attached excel files to view the Invigilators Assigning for Mid-2 Examination',
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],
      )
    file_path = os.path.join(BASE_DIR,f'{user_name}_Invigilators_Details.xlsx')
    with open(file_path,'rb') as f:
      excel_file=f.read()
      file_name=f'{user_name}_Invigilators_Details.xlsx'
      email.attach(file_name,excel_file,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
    return 'Email Sent'
  
  except FileNotFoundError:
    return f'File {file_path} not found'
  except Exception as e:
    return f'Error: {str(e)}'

@shared_task(bind=True)
def mail_to_each_student(self,exam_date,time_str,pin_number,name,room_number,seat_no,to_mail):
  try:
    email=EmailMessage(
      subject=f'Your Seat Allotment for exam on {exam_date} at {time_str}',
      body=f'Your Pin= {pin_number}, Name{name}. Your Seat number for the examination conducting on {exam_date} at {time_str} is Seat= {seat_no} of Room= {room_number}',
      from_email=settings.EMAIL_HOST_USER,
      to=[to_mail],
    )
    email.send()
    return 'Email Sent'
  except Exception as e:
    return f'Error: {str(e)}'

@shared_task(bind=True)
def mail_to_each_invigilator(self,exam_date,exam_time,unique_no,to_mail,room,name):
  try:
    email=EmailMessage(
      subject=f'Invigilation for exam on {exam_date} at {exam_time}',
      body=f"Your ID= {unique_no}, Name= {name}. You are Assigned with the Room-{room}. Don't let the Students cheat to cheat",
      from_email=settings.EMAIL_HOST_USER,
      to=[to_mail]
    )
    email.send()
    return 'Email Sent'
  except Exception as e:
    return f'Error: {str(e)}'
      

  
  