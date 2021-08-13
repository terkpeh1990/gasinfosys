# from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings
# from datetime import datetime,date
# from django.contrib.sessions.models import Session
# from django.core.validators import MaxValueValidator
# from django.db.models.signals import post_save,pre_save
# from django.dispatch import receiver
# from amis.settings import EMAIL_HOST_USER
# from django.core.mail import send_mail,EmailMessage
# import uuid
# from .utils import id_generator,incrementor
#
# # Create your models here.
# User = settings.AUTH_USER_MODEL
#
# class Grade(models.Model):
#     grade_name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.grade_name
#
# class Prority(models.Model):
#     level_name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.level_name
#
# class Region(models.Model):
#     region_name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.region_name
#
# class District(models.Model):
#     districtname = models.CharField(max_length=100)
#     region = models.ForeignKey(Region,blank=True,null=True, on_delete= models.CASCADE)
#
#     def __str__(self):
#         return self.districtname
#
# class Status(models.Model):
#     status_name = models.CharField(max_length= 100)
#
#     def __str__(self):
#         return self.status_name
#
# class agent_Status(models.Model):
#     astatus_name = models.CharField(max_length= 100)
#
#     def __str__(self):
#         return self.astatus_name
#
# class Category(models.Model):
#     category_name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.category_name
#
# class UserSession(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     session = models.OneToOneField(Session, on_delete=models.CASCADE)
#
# class Profile(models.Model):
#     user = models.OneToOneField(User,blank=True,null=True, on_delete= models.CASCADE)
#     name = models.CharField(max_length=200,null=True,blank=True)
#     email = models.CharField(max_length=200,null=True,blank=True)
#     telephone = models.CharField(max_length=20)
#     grade = models.ForeignKey(Grade,null=True,on_delete= models.CASCADE)
#     region = models.ForeignKey(Region,blank=True,null=True, on_delete= models.CASCADE)
#     district = models.ForeignKey(District,blank=True,null=True, on_delete= models.CASCADE)
#     is_staff = models.BooleanField(default=False)
#     is_agent = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_director = models.BooleanField(default=False)
#     is_new = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.name
#
#
# class Team(models.Model):
#     team_name = models.CharField(max_length= 100)
#     def __str__(self):
#         return self.team_name
#
#
# class Technician(models.Model):
#     technician = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.technician.name
#
# class Ticket(models.Model):
#     ess =(
#     ('Escalate','Escalate'),
#     )
#
#     name = models.ForeignKey(Profile,null=True,blank=True,on_delete= models.CASCADE)
#     subject = models.CharField(max_length=200,null=True,blank=True)
#     description = models.CharField(max_length=200,null=True,blank=True)
#     region = models.CharField(max_length=200,null=True,blank=True)
#     district = models.CharField(max_length=200,null=True,blank=True)
#     category = models.ForeignKey(Category,null=True,blank=True,on_delete= models.CASCADE)
#     status = models.ForeignKey(Status,null=True,blank=True,on_delete= models.CASCADE)
#     astatus = models.ForeignKey(agent_Status,null=True,blank=True,on_delete= models.CASCADE)
#     prority = models.ForeignKey(Prority,null=True,blank=True,on_delete= models.CASCADE)
#     agent = models.ForeignKey(Technician,null=True,blank=True,on_delete= models.CASCADE)
#     agent_team = models.ForeignKey(Team,null=True,blank=True,on_delete= models.CASCADE)
#     ticket_date = models.DateField()
#     expected_date = models.DateField(null=True,blank=True)
#     escalated = models.CharField(max_length = 60, choices = ess )
#     remarks = models.CharField(max_length=200,null=True,blank=True)
#     close_date =models.DateField(null=True,blank=True)
#
#     def __str__(self):
#         return self.subject
#
#     class Meta():
#         ordering = ["-id"]
#
#
#     # def save(self):
#     #     if not self.id:
#     #         number = incrementor()
#     #         self.id = "AS" +"-" + "TN" +"-"+ str(number())
#     #         while Ticket.objects.filter(id=self.id).exists():
#     #             self.id = "AS" +"-" + "TN" +"-"+ str(number())
#     #     super(Ticket, self).save()
#
#
# # @receiver(post_save, sender=Ticket)
# # def send_mail(sender, instance,created, **kwargs):
# #     user_email = instance.name.email
# #     ticket_id = instance.id
# #     subjects = instance.subject
# #     description = instance.description
# #     status = instance.status
# #     to =user_email
# #         # from_email =EMAIL_HOST_USER
# #     html_content = "You have succesfully generated a ticket.<br>Details:<br>TIcket ID : %s <br> Describtion  : %s <br> Ticket Status : %s <br><br><br>Thank You <br>IT HELPDESK"
# #     body= html_content %(ticket_id,description,status)
# #     subject =subjects
# #         # message=EmailMessage(subject=subject',body,EMAIL_HOST_USER,[to])
# #     message=EmailMessage(subject,body,EMAIL_HOST_USER,[to])
# #     message.content_subtype='html'
# #     message.send()
#
#
# class AssignedTicket(models.Model):
#     ticketid= models.CharField(max_length=20, unique=True, primary_key=True,editable=False)
#     name = models.ForeignKey(Profile,null=True,blank=True,on_delete= models.CASCADE)
#     subject = models.CharField(max_length=200,null=True,blank=True)
#     description = models.CharField(max_length=200,null=True,blank=True)
#     prority = models.ForeignKey(Prority,null=True,blank=True,on_delete= models.CASCADE)
#     ticket_date = models.DateField()
#     expected_date = models.DateField(null=True,blank=True)
#     status = models.ForeignKey(Status,null=True,blank=True,on_delete= models.CASCADE)
#     astatus = models.ForeignKey(agent_Status,null=True,blank=True,on_delete= models.CASCADE)
#
#     def __str__(self):
#         return self.subject
#
# # @receiver(pre_save, sender=AssignedTicket)
# # def send_mail(sender, instance, **kwargs):
# #     user_email = instance.name.email
# #     ticket_id = instance.ticketid
# #     subjects = instance.subject
# #     description = instance.description
# #     status = instance.status
# #     to =user_email
# #
# #     html_content = "Ticket with the details below has been assigned to you.<br>Details:<br>TIcket ID : %s <br> Describtion  : %s <br> Ticket Status : %s <br><br><br>Thank You <br>IT HELPDESK"
# #     body= html_content %(ticket_id,description,status)
# #     subject =subjects
# #
# #     message=EmailMessage(subject,body,EMAIL_HOST_USER,[to])
# #     message.content_subtype='html'
# #     message.send()
#
#
# class EscalatedTicket(models.Model):
#     ticketid= models.CharField(max_length=20, unique=True, primary_key=True,editable=False)
#     name = models.ForeignKey(Profile,null=True,blank=True,on_delete= models.CASCADE)
#     subject = models.CharField(max_length=200,null=True,blank=True)
#     description = models.CharField(max_length=200,null=True,blank=True)
#     ticket_date = models.DateField(null=True,blank=True)
#     expected_date = models.DateField(null=True,blank=True)
#     status = models.ForeignKey(Status,null=True,blank=True,on_delete= models.CASCADE)
#     astatus = models.ForeignKey(agent_Status,null=True,blank=True,on_delete= models.CASCADE)
#
#
#     def __str__(self):
#         return self.subject
#
# # @receiver(pre_save, sender=EscalatedTicket)
# # def send_mail(sender, instance, **kwargs):
# #     user_email = instance.name.email
# #     ticket_id = instance.ticketid
# #     subjects = instance.subject
# #     description = instance.description
# #     status = instance.status
# #     to =user_email
# #
# #     html_content = "Ticket with the details below has been escalated to you.<br>Details:<br>TIcket ID : %s <br> Describtion  : %s <br> Ticket Status : %s <br><br><br>Thank You <br>IT HELPDESK"
# #     body= html_content %(ticket_id,description,status)
# #     subject =subjects
# #
# #     message=EmailMessage(subject,body,EMAIL_HOST_USER,[to])
# #     message.content_subtype='html'
# #     message.send()
#
# class Ticket_Comments(models.Model):
#     ticket_id = models.ForeignKey(Ticket,on_delete= models.CASCADE)
#     content = models.CharField(max_length=700)
#     agent = models.ForeignKey(Technician,on_delete= models.CASCADE)
#     creation_date = models.DateField(validators=[MaxValueValidator(limit_value=date.today)])
#     # last_updated = models.DateTimeField()
#
#     def __str__(self):
#         return self.content
#
# class Escalate(models.Model):
#     ticket_id = models.ForeignKey(Ticket,on_delete= models.CASCADE)
#     agent = models.ForeignKey(Technician,on_delete= models.CASCADE)
#     agent_team = models.ForeignKey(Team,null=True,blank=True,on_delete= models.CASCADE)
#     escalated_date = models.DateField()
#     reason = models.CharField(max_length=700)
#
#     def __str__(self):
#         return self.agent.technician.name
#
# class History(models.Model):
#     ticket_id = models.ForeignKey(Ticket,on_delete= models.CASCADE)
#     agent = models.ForeignKey(Technician,on_delete= models.CASCADE)
#     creation_date = models.DateField(validators=[MaxValueValidator(limit_value=date.today)])
#     last_updated =  models.DateField()
#     solved_date = models.DateField()
#     staff = models.ForeignKey(Profile,on_delete= models.CASCADE)
