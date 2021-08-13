from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, View, CreateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from auditservice.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from django.core.mail import send_mail,EmailMessage


def create_requisition(request):
    u = request.user.id
    profile = Profile.objects.get(user = u)
    head = Supervisor.objects.get(unit = profile.district)
    req = Requisition.objects.create(status="Pending", staff = profile, department = profile.district, unit_head =head)
    request.session['id'] = req.id
    return redirect('inventory:add_requisition_details')


class add_requisition_details(CreateView):
    model = Requisition_Details
    paginate_by = 5
    form_class = RequisitionForm
    template = 'inventory/requisitionform.html'

    def get(self, *args, **kwargs):
        if self.request.session['id']:
            ids = self.request.session['id']
            req = Requisition.objects.get(id=ids)
            form = self.form_class()
            detail = Requisition_Details.objects.filter(requisition_id=req)

            return render(self.request, self.template, {"form": form, "detail": detail})

    def post(self,  *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if self.request.session['id']:
                ids = self.request.session['id']
                req = Requisition.objects.get(id=ids)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.requisition_id = req
                instance.save()
                messages.success(self.request, instance.product.name +" " +"added successfully")
                ser_instance = serializers.serialize('json', [instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
                
            else:
               
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": "Quantity cannot be more than the avialable stock "}, status=400)

    def form_valid(self, form):
        messages.success(self.request,  "Item Added Successfully.To see the item please click on Set")
        return super().form_valid(form)
    
    

def dones(request):
    try:
        if request.session['id']:
            ids = request.session['id']
            req = Requisition.objects.get(id=ids)
            req.check=True
            req.save()
            del request.session['id']  
            if request.user.profile.is_staff:
                return redirect('inventory:User_dashboard')
            elif request.user.profile.is_hod:
                return redirect('inventory:Hoddashboard')
            elif request.user.profile.is_stores:
                return redirect('inventory:Stores_dashboard')
            else:
                return redirect('inventory:Admin_dashboard')
    except KeyError:
        pass

def pending_requisition(request):
    us = Profile.objects.get(user = request.user.id)
    sup = Supervisor.objects.get(profile_staff=us)
    req = Requisition.objects.filter(status="Pending", unit_head=sup)
    
    paginator = Paginator(req, 5)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    
    template = 'inventory/pending_requisition.html'
    context ={
        'req': req,
        'page_obj': page_obj,
        
    }
    
    return render(request, template, context)
    
    
def view_request(request,pk):
    req = Requisition.objects.get(id=pk)
    detail = Requisition_Details.objects.filter(requisition_id=pk)
    
    template = 'inventory/view_request.html'
    context ={
        'req': req,
        'detail': detail,
    }
    return render(request, template, context)
    
def approve_request(request,pk):
    req = Requisition.objects.get(id=pk)
    req.status = "Awaiting Approval"
    req.save()
    
    messages.success(request, "Requisition Has been sent to Administration for approval")
    return redirect('inventory:hod_view_request', pk=req.id)


def awaiting_requisition(request):
    req = Requisition.objects.filter(status="Awaiting Approval")

    template = 'inventory/awaiting_approval.html'
    context = {
        'req': req,
        
    }

    return render(request, template, context)


def admin_view_request(request, pk):
    req = Requisition.objects.get(id=pk)
    detail = Requisition_Details.objects.filter(requisition_id=pk)

    template = 'inventory/admin_view_request.html'
    context = {
        'req': req,
        'detail': detail,
    }
    return render(request, template, context)

def hod_view_request(request, pk):
    req = Requisition.objects.get(id=pk)
    detail = Requisition_Details.objects.filter(requisition_id=pk)

    template = 'inventory/hod_view_request.html'
    context = {
        'req': req,
        'detail': detail,
    }
    return render(request, template, context)

def approve_quantity(request, pk):
    det = Requisition_Details.objects.get(id=pk)
    item_inventory = Inventory.objects.get(product_id = det.product)
    cc = item_inventory.avialable_stock -item_inventory.restock_level
    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity_issued']
            if qty > cc:
                messages.success(request, "Qantity approved cannot be more than" + " " + str(cc))
                return redirect('inventory:approve_quantity', pk = det.id)
            else:
                det.quantity_issued = form.cleaned_data['quantity_issued']
                det.save()
                messages.success(request,"Approved Quantity Entered")
                return redirect('inventory:admin_view_request', pk=det.requisition_id)
    else:
        
        form = QuantityForm()
    template = 'inventory/approve_quantity.html'
    context = {
        'form': form,
        'item_inventory': item_inventory,
        'cc': cc,
        }
    return render(request, template, context)


def admin_approve_request(request, pk):
    req = Requisition.objects.get(id=pk)
    details = Requisition_Details.objects.filter(requisition_id=req.id)
    for products in details:
        try:
            product = Product.objects.get(id=products.product_id)
            get_product = Inventory.objects.get(product_id=product.id)
            get_product.yet_to_recieve += products.quantity_issued
            get_product.save()

        except Inventory.DoesNotExist:
            pass
    req.status = "Approved"
    req.save()
    messages.success(
        request, "Requisition Has been sent to Stores to be issued")
    return redirect('inventory:admin_view_request', pk=req.id)
    

def approved_requisition(request):
    req = Requisition.objects.filter(status="Approved")

    template = 'inventory/approved_requisition.html'
    context = {
        'req': req,

    }
    return render(request, template, context)


def stores_view_request(request, pk):
    req = Requisition.objects.get(id=pk)
    detail = Requisition_Details.objects.filter(requisition_id=pk,status=False)

    template = 'inventory/stores_view_request.html'
    context = {
        'req': req,
        'detail': detail,
    }
    return render(request, template, context)

def issue_requisition(request,pk):
    req = Requisition.objects.get(id=pk)
    details = Requisition_Details.objects.filter(requisition_id=req.id)
    for products in details:
        try:
            product = Product.objects.get(id=products.product_id)
            get_product = Inventory.objects.get(product_id=product.id)
            get_product.yet_to_recieve -= products.quantity_issued
            get_product.outgoing += products.quantity_issued
            get_product.save()
            Inventory_records.objects.create(
                product=product, quantity=products.quantity_issued, status="Outgoing")

        except Inventory.DoesNotExist:
            pass
    # Inventory_records.objects.create(
    #     product=products, quantity=req.quantity_accepted, status="Incoming")
    req.status = "Issued"
    req.save()
    messages.success(
        request, "Requisition Issued Successfully")
    return redirect('inventory:stores_view_request', pk=req.id)
    
def done(request):
    if request.user.profile.is_staff:
        return redirect('inventory:User_dashboard')
    elif request.user.profile.is_hod:
        return redirect('inventory:Hoddashboard')
    elif request.user.profile.is_stores:
        return redirect('inventory:Stores_dashboard')
    else:
        return redirect('inventory:Admin_dashboard')

def user_requisition(request):
    
    total = Requisition.objects.filter(
        staff=request.user.profile).order_by('-id')
    

    template = 'inventory/user_requisition.html'
    context = {
        'total': total, 
               }
    return render(request, template, context)


def deletes(request, pk):
    pro = Requisition_Details.objects.get(id=pk)
    pro.delete()
    messages.success(request,'Item Removed')
    return redirect('inventory:add_requisition_details')

def issue_item(request, pk):
    requests = Requisition_Details.objects.get(id=pk)
    req = Requisition.objects.get(id = requests.requisition_id)
    product = Product.objects.get(id = requests.product.id)
    items = Inventory_Stock_Record.objects.filter(product_id=product,issued=False)[:requests.quantity_issued]
    for item in items:
        item.issued = True
        item.issued_to = req.staff
        item.save()
    try:
        get_product = Inventory.objects.get(product_id=product)
        get_product.yet_to_recieve -= requests.quantity_issued
        get_product.outgoing += requests.quantity_issued
        get_product.save()
        Inventory_records.objects.create(
                product=product, quantity=requests.quantity_issued, status="Outgoing")

    except Inventory.DoesNotExist:
        pass
    req.status = "Issued"
    req.save()
    requests.status = "True"
    requests.save()
    messages.success(request,"Item Issued")
    return redirect('inventory:stores_view_request', pk=req.id)
    
