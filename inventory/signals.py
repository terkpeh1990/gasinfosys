from django.db.models.signals import post_save
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver
from .models import Profile,UserSession
from django.shortcuts import redirect
# from django.core.mail import send_mail,EmailMessage
from .import models
from django.contrib.sessions.models import Session
from .import views
from .models import *
from twilio.rest import TwilioRestClient
from twilio.rest import Client
from auditservice.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from django.core.mail import send_mail, EmailMessage


def customer_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='standarduser')
		instance.groups.add(group)

		Profile.objects.create(
			user=instance,
			name=instance.first_name +" "+ instance.last_name,
			email =instance.email,
			is_staff = True,
			is_new = True,

			)
		print('Profile created!')

post_save.connect(customer_profile, sender=User)


@receiver(user_logged_in)
def remove_other_sessions(sender, user, request, **kwargs):
    # remove other sessions
    Session.objects.filter(usersession__user=user).delete()


    # save current session
    request.session.save()

    # create a link from the user to the current session (for later removal)
    UserSession.objects.get_or_create(
        user=user,
        session=Session.objects.get(pk=request.session.session_key)
	)
    return redirect('log')

def requisition_notification(sender, instance, created, **kwargs):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    if instance.status == 'Pending' and instance.check:
        try:
            subject = "Requisition"
            message = "Dear"+ " " + instance.staff.name +","+ " " +"Your requisition with batch number" + " " + str(instance.id) + " "+ "has been sent for approval. You will be notified when it is ready" 
            message2 ="Dear"+ " " + instance.unit_head.profile_staff.name +","+ " " + "Requisition with batch number" + " " + str(instance.id) + " "+ "has been brougth to you attention for approval."
            sender = EMAIL_HOST_USER
            to = [instance.staff.email]
            to2 = [instance.unit_head.profile_staff.email]
            send_mail(subject, message, sender, to, fail_silently=False)
            send_mail(subject, message2, sender, to2, fail_silently=False)
        except IOError:
            print('fail')
            pass
        

        try:
            message = client.messages.create(
                to="+233" + instance.staff.telephone,
                from_=TWILIO_PHONE_NUMBER,
                body="Dear" + " " + instance.staff.name + ","+" " + "Your requisition with batch number" + " " + str(instance.id) + " " + "has been sent for approval. You will be notified when it is ready")
        except IOError:
            print('fail')
            pass
        
        try:
            message = client.messages.create(
                to="+233" + instance.unit_head.profile_staff.telephone,
                from_=TWILIO_PHONE_NUMBER,
                body="Dear" + " " + instance.unit_head.profile_staff.name +","+ " " + "Requisition with batch number" + " " + str(instance.id) + " " + "has been brougth to you attention for approval.")
        except IOError:
            print('fail')
            pass
        
    elif instance.status == 'Awaiting Approval':
        try:
            location = District.objects.get(districtname="F&A")
            adms = Supervisor.objects.get(unit=location.id)
            subject = "Requisition"
            message = "Dear"+ " " + instance.staff.name +","+ " " +"Your requisition with batch number" + " " + str(instance.id) + " "+ "has been sent to administration for approval. You will be notified when it is ready" 
            message2 = "Dear"+ " " + adms.profile_staff.name + ","+" " +"Requisition with batch number" + " " + str(instance.id) + " "+ "has been brougth to you attention for approval."
            sender = EMAIL_HOST_USER
            
            to = [instance.staff.email]
            to2 = [adms.profile_staff.email]
            send_mail(subject, message, sender, to, fail_silently=False)
            send_mail(subject, message2, sender, to2, fail_silently=False)
        except IOError:
            print('fail')
            pass
        try:
            message = client.messages.create(
                to="+233" + instance.staff.telephone,
                from_=TWILIO_PHONE_NUMBER,
                body="Dear" + " " + instance.staff.name +","+ " " + "Your requisition with batch number" + " " + str(instance.id) + " " + "has been sent to administration for approval. You will be notified when it is ready")
        except IOError:
            print('fail')
            pass
        try:
            message = client.messages.create(
                to="+233" + adms.profile_staff.telephone,
                from_=TWILIO_PHONE_NUMBER,
                body="Dear"+ " " + adms.profile_staff.name +","+ " " +"Requisition with batch number" + " " + str(instance.id) + " "+ "has been brougth to you attention for approval.")
        except IOError:
            print('fail')
            pass
    elif instance.status == 'Approved':
        try:
            subject = "Requisition"
           
            message = "Dear" + " " + instance.staff.name +","+ " " + "Your requisition with batch number" + " " + \
            	str(instance.id) + " " + \
                "has been approved. Please pass by the stores unit at the Head office to pickup your item(s). You will be required to provide the unique batch number before pickup"
                
            sender = EMAIL_HOST_USER
            to = [instance.staff.email]
            send_mail(subject, message, sender, to, fail_silently=False)
        except IOError:
            print('fail')
            pass
        
        try:
            message = client.messages.create(
                to="+233" + instance.staff.telephone,
                from_=TWILIO_PHONE_NUMBER,
                body="Dear" + " " + instance.staff.name + "," + " " + "Your requisition with batch number" + " " +
            	str(instance.id) + " " +
                "has been approved. Please pass by the stores unit at the Head office to pickup your item(s). You will be required to provide the unique batch number before pickup")
        except IOError:
            print('fail')
            pass


post_save.connect(requisition_notification, sender=Requisition)
