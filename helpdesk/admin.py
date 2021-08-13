from django.contrib import admin
from helpdesk.models import Profile, Grade, Region, District, Ticket, Status, agent_Status, Technician, Team, Ticket_Comments, AssignedTicket, Prority, EscalatedTicket, Category, Escalate, Supervisor, Checkid

# Register your models here.

admin.site.register(Category)

admin.site.register(Ticket)
admin.site.register(Escalate)
admin.site.register(Status)
admin.site.register(agent_Status)
admin.site.register(Technician)
admin.site.register(Team)
admin.site.register(Ticket_Comments)
admin.site.register(AssignedTicket)
admin.site.register(EscalatedTicket)
admin.site.register(Prority)
admin.site.register(Supervisor)
admin.site.register(Checkid)
