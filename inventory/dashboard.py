from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
import datetime
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth
import json



def User_dashboard(request):
    today = datetime.datetime.now()
    object_status_list = ["Approved", "Issued"]
    print(request.user.username)
    total = request.user.profile.requisition_set.all().order_by('-id')
    total_requisition = total.filter(requisition_date__year=today.year).count()
    total_requisition_yearly = total.filter(requisition_date__year=today.year)
    total_approved_requisition = total.filter(status="Approved", requisition_date__year=today.year).count()
    total_issued_requisition = total.filter(status="Issued", requisition_date__year=today.year).count()
    total_pending_requisition = total.filter(
        requisition_date__year=today.year).exclude(status__in=object_status_list).count()
    
    status_group = total_requisition_yearly.values(
        'status').annotate(Monthly=Count('id'))
    
    # data = []
    # for s in status_group:
    #     data.append(s.Monthly)
    
    context = {
        
        'total': total,
        'total_requisition': total_requisition,
        'total_approved_requisition': total_approved_requisition,
        'total_issued_requisition': total_issued_requisition,
        'total_pending_requisition': total_pending_requisition,
        'status_group': status_group,
        'total_requisition_yearly': total_requisition_yearly,
        # 'data': data,
        
    }
        
    template = "inventory/userdashboard.html"
    return render(request,template,context)
    

def Hoddashboard(request):
    today = datetime.datetime.now()
    object_status_list = ["Approved", "Issued"]
    # total = request.user.profile.requisition_set.all().order_by('-id')
    total = Requisition.objects.filter(department = request.user.profile.district)
    total_requisition = total.filter(requisition_date__year=today.year).count()
    total_requisition_yearly = total.filter(requisition_date__year=today.year)
    total_approved_requisition = total.filter(
        status="Approved", requisition_date__year=today.year).count()
    total_issued_requisition = total.filter(
        status="Issued", requisition_date__year=today.year).count()
    total_pending_requisition = total.filter(
        requisition_date__year=today.year).exclude(status__in=object_status_list).count()

    status_group = total_requisition_yearly.values(
        'status').annotate(Monthly=Count('id'))
    # statu = total_requisition_yearly.status
   
        
    context = {

        'total': total,
        'total_requisition': total_requisition,
        'total_approved_requisition': total_approved_requisition,
        'total_issued_requisition': total_issued_requisition,
        'total_pending_requisition': total_pending_requisition,
        'status_group': status_group,
        'total_requisition_yearly': total_requisition_yearly,
        

    }

    template = "inventory/userdashboard.html"
    return render(request, template, context)
    

def Admin_dashboard(request):
    today = datetime.datetime.now()
    object_status_list = ["Approved", "Issued"]
    # total = request.user.profile.requisition_set.all().order_by('-id')
    total = Requisition.objects.all()
    total_requisition = total.filter(requisition_date__year=today.year).count()
    total_requisition_yearly = total.filter(
        requisition_date__year=today.year, status="Awaiting Approval")
    total_approved_requisition = total.filter(
        status="Approved", requisition_date__year=today.year).count()
    total_issued_requisition = total.filter(
        status="Issued", requisition_date__year=today.year).count()
    total_pending_requisition = total.filter(
        requisition_date__year=today.year).exclude(status__in=object_status_list).count()

    status_group = total_requisition_yearly.values(
        'status').annotate(Monthly=Count('id'))
    # statu = total_requisition_yearly.status

    context = {

        'total': total,
        'total_requisition': total_requisition,
        'total_approved_requisition': total_approved_requisition,
        'total_issued_requisition': total_issued_requisition,
        'total_pending_requisition': total_pending_requisition,
        'status_group': status_group,
        'total_requisition_yearly': total_requisition_yearly,


    }

    template = "inventory/userdashboard.html"
    return render(request, template, context)


def Stores_dashboard(request):
    today = datetime.datetime.now()
    object_status_list = ["Approved", "Issued"]
    # total = request.user.profile.requisition_set.all().order_by('-id')
    total = Requisition.objects.all()
    total_requisition = total.filter(requisition_date__year=today.year).count()
    total_requisition_yearly = total.filter(
        requisition_date__year=today.year, status="Approved")
    total_approved_requisition = total.filter(
        status="Approved", requisition_date__year=today.year).count()
    total_issued_requisition = total.filter(
        status="Issued", requisition_date__year=today.year).count()
    total_pending_requisition = total.filter(
        requisition_date__year=today.year).exclude(status__in=object_status_list).count()

    status_group = total_requisition_yearly.values(
        'status').annotate(Monthly=Count('id'))
    # statu = total_requisition_yearly.status

    context = {

        'total': total,
        'total_requisition': total_requisition,
        'total_approved_requisition': total_approved_requisition,
        'total_issued_requisition': total_issued_requisition,
        'total_pending_requisition': total_pending_requisition,
        'status_group': status_group,
        'total_requisition_yearly': total_requisition_yearly,


    }

    template = "inventory/userdashboard.html"
    return render(request, template, context)
