from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .filters import *
import datetime
from django.db.models import Q, Sum, Count, F
from django.db.models.functions import TruncMonth
from django.contrib import messages

def total_requisitions(request):
    
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
    
    
    myFilter = RequisitionFilter(request.GET, queryset=total)
    total = myFilter.qs
    total_requisition = total.count()
    total_approved_requisition = total.filter(status="Approved").count()
    total_issued_requisition = total.filter(status="Issued").count()
    total_pending_requisition = total.filter().exclude(status__in=object_status_list).count()
    

    template = 'inventory/total_requisition.html'
    context ={
        'total': total,
        'total_requisition': total_requisition,
        'total_approved_requisition': total_approved_requisition,
        'total_issued_requisition': total_issued_requisition,
        'total_pending_requisition': total_pending_requisition,
        'total_requisition_yearly': total_requisition_yearly,
         'myFilter':myFilter,
    }
    return render(request, template, context)


def product_forcast(request):
    total = Product.objects.all()
    forcast = total.values('name').annotate(
        qty=Sum('requisition_details__quantity'), qtyissued=Sum('requisition_details__quantity_issued')).order_by('name')
    
   
    
    template = 'inventory/forcast.html'
    context = {
        'forcast': forcast,
       
    }
    return render(request, template, context)
    

def yearly_forcast(request):
    total = Product.objects.all()
    forcast = Product.objects.values('name').annotate(
        month=TruncMonth('requisition_details__detail_date'), qty=Sum('requisition_details__quantity'), qtyissued=Sum('requisition_details__quantity_issued')).order_by('-requisition_details__detail_date')
   
    template = 'inventory/date_forcast.html'
    context = {
        'forcast': forcast,

    }
    return render(request, template, context)

def manage_inventory(request):
    inventory = Inventory.objects.all()
    template = 'inventory/inventory.html'
    context = {
        'inventory': inventory,
    }
    return render(request, template, context)

def manage_closing_stock(request):
    closingstock = Closing_stocks.objects.all()
    template = 'inventory/closingstock.html'
    context = {
        'closingstock':closingstock,
    }
    return render(request, template, context)


def closing_stock(request):
    inventorys = Inventory.objects.all()
    for inventory in inventorys:
        product = Product.objects.get(id=inventory.product_id.id)
        Closing_stocks.objects.create(
            product=product, closing_stock=inventory.avialable_stock)
    messages.success(request, 'Stock Closed')
    return redirect('inventory:manage_inventory')

def restocking_level(request):
    stock = Inventory.objects.filter(avialable_stock__lte= F('restock_level'))
    template = 'inventory/restock_level.html'
    context = {
        'stock': stock,
    }
    return render(request, template, context)
    
def Item_issued(request):
    items =Inventory_Stock_Record.objects.all()
    template = 'inventory/issue_records.html'
    context = {
        'items': items,
    }
    return render(request, template, context)