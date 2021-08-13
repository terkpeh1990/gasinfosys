from django.urls import path
from .import views


app_name = 'helpdesk'

urlpatterns = [
    

    path('ajax/load-district/', views.load_district, name="ajax_load_cities"),
    path('ajax/load-agent/', views.load_agent, name="ajax_load_agent"),
    path('ajax/load-supervisor/', views.load_supervisor,
         name="ajax_load_supervisor"),

    path('userdashbord/', views.user_dashboard, name="userdashboard"),
    path('Newticket/', views.user_ticket, name="userticket"),
    path('edit/<str:pk>/', views.edit_user_ticket, name="edituserticket"),
    path('ticketdetail/<str:pk>/', views.view_user_ticket,
         name="userticketdetails"),


    path('ticket/', views.agent_ticket, name="ticket"),
    path('editticket/<str:pk>/', views.edit_agent_ticket, name="editticket"),
    path('detail/<str:pk>/', views.detail_agent_ticket, name="detail"),
    path('agentdashbord/', views.agent_dashboard, name="agentdashboard"),
    path('ticketescalated/', views.agent_escalated, name="ticketescalated"),
    path('escaladeticket/<str:pk>/', views.escalate_ticket, name="escaladeticket"),
    path('waitingescalate/<str:pk>/',
         views.reassign_ticket, name="waitingescalate"),
    path('awaitingticket/', views.waiting_tickets, name="awaitingticket"),
    path('waitingclosure/', views.waiting_closure, name="waitingclosure"),
    path('website/', views.website_ticket, name="website"),


    path('helpdeskdashbord/', views.helpdesk_dashboard, name="helpdeskdashboard"),
    path('edittickethelp/<str:pk>/',
         views.edit_heldesk_ticket, name="edittickethelp"),
    # path('helpdeskticket/<str:pk>/',views.heldesk_ticketedit, name="helpdeskticket"),


    path('close/<str:pk>/', views.closeticket, name="closeticket"),

    path('agentsearch/', views.agent_search, name="agentsearch"),
    path('search/', views.search, name="search"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dirsearch/', views.dirsearch, name="dirsearch"),


    path('opened/', views.open_ticket, name="open"),
    path('closed/', views.closed_ticket, name="closed"),
    path('solved/', views.solved_ticket, name="solved"),
    path('total/', views.total_ticket, name="total"),

    path('delayedtickets/', views.delaytickets, name="delayedtickets"),
    path('solvedontime/', views.ontime, name="solvedontime"),
    path('notsolvedontime/', views.notontime, name="notsolvedontime"),
    path('auditlog/', views.audittrail, name="auditlog"),
    path('sup/', views.sup, name="sup"),



]
