from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, date, timezone
from django.contrib.sessions.models import Session
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMessage
import uuid
from .utils import id_generator, incrementor
from auditservice.settings import EMAIL_HOST_USER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
# , proxy_client
from twilio.rest import Client
import datetime
from django.utils import timezone
from simple_history.models import HistoricalRecords
from inventory.models import *
from inventory.models import Profile

# Create your models here.
User = settings.AUTH_USER_MODEL




class Prority(models.Model):
    level_name = models.CharField(max_length=100)

    def __str__(self):
        return self.level_name





class Status(models.Model):
    status_name = models.CharField(max_length=100)

    def __str__(self):
        return self.status_name


class agent_Status(models.Model):
    astatus_name = models.CharField(max_length=100)

    def __str__(self):
        return self.astatus_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Team(models.Model):
    team_name = models.CharField(max_length=100)

    def __str__(self):
        return self.team_name


class Technician(models.Model):
    technician = models.ForeignKey(Profile, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.technician.name


class Supervisor(models.Model):
    supervisor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.supervisor.name


class Ticket(models.Model):
    ess = (
        ('Escalate', 'Escalate'),
    )
    id = models.CharField(max_length=200, primary_key=True)
    name = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    region = models.ForeignKey(
        Region, blank=True, null=True, on_delete=models.CASCADE)
    district = models.ForeignKey(
        District, blank=True, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.CASCADE)
    status = models.ForeignKey(
        Status, null=True, blank=True, on_delete=models.CASCADE)
    astatus = models.ForeignKey(
        agent_Status, null=True, blank=True, on_delete=models.CASCADE)
    prority = models.ForeignKey(
        Prority, null=True, blank=True, on_delete=models.CASCADE)
    agent = models.ForeignKey(Technician, null=True,
                              blank=True, on_delete=models.CASCADE)
    agent_team = models.ForeignKey(
        Team, null=True, blank=True, on_delete=models.CASCADE)
    ticket_date = models.DateField()
    ticket_time = models.TimeField()
    use_date = models.DateTimeField()
    expected_date = models.DateField(null=True, blank=True)
    expected_days = models.DurationField(null=True, blank=True)
    escalated = models.CharField(max_length=60, choices=ess)
    remarks = models.CharField(max_length=200, null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    completed_days = models.DurationField(null=True, blank=True)
    elapsed_time = models.DurationField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        bb = datetime.datetime.now()
        zz = timezone.now()
        ss = datetime.date
        if not self.ticket_date:
            self.ticket_date = bb
            self.ticket_time = zz
            self.use_date = bb
        today = bb.year
        if not self.id:
            number = incrementor()
            self.id = number()
            while Ticket.objects.filter(id=self.id).exists():
                self.id = number()

        if self.prority and not self.expected_date:
            if self.prority.level_name == "High":
                self.expected_date = self.ticket_date + \
                    datetime.timedelta(days=1)
            elif self.prority.level_name == "medium":
                self.expected_date = self.ticket_date + \
                    datetime.timedelta(days=2)
            else:
                self.expected_date = self.ticket_date + \
                    datetime.timedelta(days=3)

            a = self.expected_date
            b = self.ticket_date
            delta = a - b
            self.expected_days = delta

        if self.status.status_name == "closed":
            # if self.status == "1":
            self.close_date = datetime.datetime.now(timezone.utc)
            c = self.close_date
            b = self.use_date
            delta2 = c - b
            self.completed_days = delta2
            self.elapsed_time = self.expected_days - self.completed_days
        super(Ticket, self).save(*args, **kwargs)


# @receiver(post_save, sender=Ticket)
# def send_mail(sender, instance, created, **kwargs):
#     user_name = str(instance.name)
#     tid = instance.id
#     tsub = instance.subject
#     tstatus = instance.status
#     user_phone = instance.name.telephone
#     bb = datetime.datetime.now()
#     if Ticket.objects.filter(id=tid).exists() and tstatus == "closed":

#         client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN,
#                        )
#         # http_client = proxy_client
#         try:
#             message = client.messages.create(
#                 to="+233" + user_phone,
#                 from_=TWILIO_PHONE_NUMBER,
#                 body="Dear" + " " + user_name + "," + " " + "Your ticket with the id"+" " + tid + " "+"and subject"+" "+" "+"'" + tsub+"'"+" "+" "+"has been resolved. --Thank you")
#         except IOError:
#             pass


class AssignedTicket(models.Model):
    ticketid = models.CharField(
        max_length=20, unique=True, primary_key=True, editable=False)
    name = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    prority = models.ForeignKey(
        Prority, null=True, blank=True, on_delete=models.CASCADE)
    ticket_date = models.DateField()
    expected_date = models.DateField(null=True, blank=True)
    status = models.ForeignKey(
        Status, null=True, blank=True, on_delete=models.CASCADE)
    astatus = models.ForeignKey(
        agent_Status, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class EscalatedTicket(models.Model):
    ticketid = models.CharField(
        max_length=20, unique=True, primary_key=True, editable=False)
    name = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    ticket_date = models.DateField(null=True, blank=True)
    expected_date = models.DateField(null=True, blank=True)
    status = models.ForeignKey(
        Status, null=True, blank=True, on_delete=models.CASCADE)
    astatus = models.ForeignKey(
        agent_Status, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class Ticket_Comments(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    content = models.CharField(max_length=700)
    agent = models.ForeignKey(Technician, on_delete=models.CASCADE)
    creation_date = models.DateField(
        validators=[MaxValueValidator(limit_value=date.today)])
    # last_updated = models.DateTimeField()

    def __str__(self):
        return self.content


class Escalate(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    agent = models.ForeignKey(Technician, on_delete=models.CASCADE)
    agent_team = models.ForeignKey(
        Team, null=True, blank=True, on_delete=models.CASCADE)
    escalated_date = models.DateField()
    reason = models.CharField(max_length=700)

    def __str__(self):
        return self.agent.technician.name


class WaitingEscalate(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    agent_team = models.ForeignKey(
        Team, null=True, blank=True, on_delete=models.CASCADE)
    escalated_date = models.DateField()
    reason = models.CharField(max_length=700)

    def __str__(self):
        return self.supervisor.supervisor.name


class History(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    agent = models.ForeignKey(Technician, on_delete=models.CASCADE)
    creation_date = models.DateField(
        validators=[MaxValueValidator(limit_value=date.today)])
    last_updated = models.DateField()
    solved_date = models.DateField()
    staff = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Checkid(models.Model):
    staffid = models.CharField(max_length=50)

    def __str__(self):
        return self.staffid
