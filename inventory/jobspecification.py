from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, View, CreateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from twilio.rest import TwilioRestClient
from twilio.rest import Client
from auditservice.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from django.core.mail import send_mail, EmailMessage

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def create_job_specification(request):
    if request.method == "POST":
        form = Job_SpecificationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.status = "Awaiting Certification"
            job.save()
            request.session['rviv'] = job.rviv
            messages.success(request, "Job Specification Created")
            return redirect ('inventory:add_specification_details')
    else:
        form = Job_SpecificationForm()
    
    template = "inventory/job_certification_form.html"
    context ={
        'form': form,
    }
    return render(request ,template,context)

# def add_specification_details(request):
def add_specification_details(request):
    
    if request.session['rviv']:
        rviv = request.session['rviv']
        job = Job_specification.objects.get(rviv=rviv)
        detail = Job_specification_details.objects.filter(rviv=job)
        detailcount = detail.count()
    if request.method == 'POST':
        form = Job_Specification_DetailForm(request.POST)
        if form.is_valid():
            details = Job_specification_details.objects.filter(rviv=job)
            jobs = Job_specification.objects.get(rviv=rviv)
            detailcounts = detail.count()
            if details.count() == int(job.quantity):
                messages.success(request,"Items Cannot be more than" + " " + str(job.quantity))
                return redirect('inventory:add_specification_details')
            else:
                cc=form.save(commit=False)
                cc.rviv =jobs
                cc.save()
                # messages.(request,"Items Added" )
                return redirect('inventory:add_specification_details')
    else:
        form = Job_Specification_DetailForm()
    template = 'inventory/add_job_specification_details.html'
    context = {
        'form': form,
        'detail': detail
    }
    return render(request,template, context)
    
# class add_specification_details(CreateView):
#     model = Job_specification_details
#     paginate_by = 5
#     form_class = Job_Specification_DetailForm
#     template = 'inventory/add_job_specification_details.html'



#     def get(self, *args, **kwargs):
#          if self.request.session['rviv']:
#             rviv = self.request.session['rviv']
#             job = Job_specification.objects.get(rviv=rviv)
#             form = self.form_class()
#             detail = Job_specification_details.objects.filter(rviv=job)
            
#             return render(self.request, self.template, {"form": form, "detail":detail})

#     def post(self,  *args, **kwargs):
#         if self.request.is_ajax and self.request.method =="POST":
#             form = self.form_class(self.request.POST)
#             if self.request.session['rviv']:
#                 rviv = self.request.session['rviv']
#                 job = Job_specification.objects.get(rviv =rviv)
#             if form.is_valid():
#                 instance = form.save(commit=False)
#                 instance.rviv = job
#                 instance.save()
#                 ser_instance = serializers.serialize('json', [instance, ])
#                 return JsonResponse({"instance": ser_instance}, status=200)
#             else:
#                 return JsonResponse({"error": form.errors}, status=400)
#         return JsonResponse({"error": ""}, status=400)

#     def form_valid(self,form):
#         messages.success(self.request, 'Detail Added')
#         return super().form_valid(form)


def deletes_job(request, pk):
    pro = Job_specification_details.objects.get(id=pk)
    pro.delete()
    messages.success(request, 'Item Removed')
    return redirect('inventory:add_specification_details')

def manage_job_spec(request):
    staff = request.user
    staff_profile = staff.profile.district
    department_job_spec = Job_specification.objects.filter(
        district=staff_profile)
    
    template = 'inventory/manage_job_specification.html'
    context = {
        'department_job_spec': department_job_spec,
    }
    return render(request, template, context)

def pending_job_spec(request):
    staff = request.user.id
    staff_profile = Profile.objects.get(user=staff)
    staff_location = staff_profile.district
    department_job_spec = Job_specification.objects.filter(status='Awaiting Certification', district=staff_profile)
    
    template = 'inventory/manage_job_specification.html'
    context = {
        'department_job_spec': department_job_spec,
    }
    return render(request, template, context)
    
def job_spec_view(request,pk):
    jobspec = Job_specification.objects.get(rviv =pk)
    jobspec_details = Job_specification_details.objects.filter(rviv=jobspec.rviv)
    
    template = 'inventory/view_jobs.html'
    context = {
        'jobspec': jobspec,
        'jobspec_details': jobspec_details
    }
    return render(request, template, context)
    
def Assign_Agent(request,pk):
    job = Job_specification.objects.get(rviv = pk)
    if request.method == "POST":
        form = AssignAgentForm(request.POST, instance=job, request=request)
        if form.is_valid():
            cc= form.save()
            
            try:
                subject = "Job Certification"
                message = "Dear" + " " + cc.agent.name + "," + " " + "Job specification with rviv number" + \
                    " " + str(job.rviv) + " " + \
                    "has been brought to your attention to be worked on."
                sender = EMAIL_HOST_USER
                to = [cc.agent.email]
                send_mail(subject, message, sender, to, fail_silently=False)
            except IOError:
                print('fail')
                pass
            
            try:
                message = client.messages.create(
                    to="+233" +  cc.agent.telephone,
                    from_=TWILIO_PHONE_NUMBER,
                    body="Dear" + " " + cc.agent.name + "," + " " + "Job specification with rviv number" + \
                    " " + str(job.rviv) + " " + \
                    "has been brought to your attention to be worked on.")
            except IOError:
                print('fail')
                pass
            messages.success(request,"Job Specification has been assigned to an agent")
            return redirect('inventory:job_spec_view', pk=job.rviv)
    else:
        form = AssignAgentForm(instance=job, request=request)
    template = 'inventory/assign_agent.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

def Assigned_Job(request):
    staff = request.user
    staff_profile = staff.profile.id
    department_job_spec = Job_specification.objects.filter(
        agent=staff_profile)
    
    template = 'inventory/manage_job_specification.html'
    context = {
        'department_job_spec': department_job_spec,
    }
    return render(request, template, context)

def accept_product(request,pk):
    pro = Job_specification_details.objects.get(id=pk)
    cc = pro.rviv_id
    print(cc)
    job = Job_specification.objects.get(rviv=pro.rviv_id)
    pro.status = 'Accepted'
    pro.reason = "Good Condition"
    pro.save()
    job.quantity_accepted += 1
    job.save()
    messages.success(request,"Verification Completed Successfully")
    return redirect('inventory:job_spec_view', pk=pro.rviv_id)


def reject_product(request, pk):
    pro = Job_specification_details.objects.get(id=pk)
    job = Job_specification.objects.get(rviv=pro.rviv_id)
    if request.method == "POST":
        form = ReasonForm(request.POST, instance=pro)
        form.save()
        pro.status = 'Rejected'
        pro.save()
        job.quantity_rejected += 1
        job.save()
        messages.success(request, "Verification Completed Successfully")
        return redirect('inventory:job_spec_view', pk=pro.rviv_id)
    else:
        form = ReasonForm(instance=pro)
    template = 'inventory/reason.html'
    context = {
        'form': form,
        'job': job,
    }
    return render(request, template, context)
    

def close_reason(request, pk):
    if request.session['rviv']:
        job = Job_specification.objects.get(rviv=pk)
        messages.success(request, "Sent For Specification")
    return redirect('inventory:job_spec_view', pk=job.rviv)

def complete_job_spec(request, pk):
    
    job = Job_specification.objects.get(rviv=pk)
    job.agentstatus = 'Complete'
    job.save()
    sup = Supervisor.objects.get(unit=job.agent.district)
    
    try:
        subject = "Job Certification"
        message = "Dear" + " " + sup.profile_staff.name + "," + " " + "Job specification with rviv number" + \
            " " + str(job.rviv) + " " + \
            "has been worked on, waiting for you to certify."
        sender = EMAIL_HOST_USER
        to = [sup.profile_staff.email]
        send_mail(subject, message, sender, to, fail_silently=False)
    except IOError:
        print('fail')
        pass
    try:
        message = client.messages.create(
            to="+233" + sup.profile_staff.telephone,
            from_=TWILIO_PHONE_NUMBER,
            body="Dear" + " " + sup.profile_staff.name + "," + " " + "Job specification with rviv number" + \
            " " + str(job.rviv) + " " + \
            "has been worked on, waiting for you to certify.")
    except IOError:
        print('fail')
        pass
    messages.success(request, "Sent For Certification")
    return redirect('inventory:Assigned_Job')

def certify(request,pk):
    restock = Job_specification.objects.get(rviv=pk)
    
    try:
        product = Product.objects.get(id=restock.product_id)
        get_product = Inventory.objects.get(product_id=product.id)
        get_product.instock += restock.quantity
        get_product.restock_level = product.restock_level
        get_product.save()
        

    except Inventory.DoesNotExist:
        product = Product.objects.get(id=restock.product_id)
        Inventory.objects.create(
            product_id=product,instock=restock.quantity_accepted, restock_level=product.restock_level)
    products = Product.objects.get(id=restock.product_id)
    restock.status = "Certified"
    restock.control = "Complete"
    restock.save()
    Inventory_records.objects.create(
        product=products, quantity=restock.quantity_accepted, status="Incoming")
    
    job_detail = Job_specification_details.objects.filter(rviv=restock)
    for items in job_detail:
        Inventory_Stock_Record.objects.create(product_id=products,serial_number=items.serial_number,description=items.description,rviv=restock)
    messages.success(request, 'Restock Certified')
    return redirect('inventory:job_spec_view', pk=restock.rviv)
    
def doness(request):
    try:
        if request.session['rviv']:
            ids = request.session['rviv']
            req = Job_specification.objects.get(rviv=ids)
            req.check=True
            req.save()
            sup =Supervisor.objects.get(unit=req.district)
            try:
                
                subject = "Job Certification"
                message = "Dear" + " " + sup.profile_staff.name + "," + " " + "Job specification with rviv number" + \
                    " " + str(req.rviv) + " " + \
                    "has been brought to your attention for certification."
                sender = EMAIL_HOST_USER
                to = [sup.profile_staff.email]
                send_mail(subject, message, sender, to, fail_silently=False)
            except IOError:
                print('fail')
                pass
            
            try:
                message = client.messages.create(
                    to="+233" + sup.profile_staff.telephone,
                    from_=TWILIO_PHONE_NUMBER,
                    body="Dear" + " " + sup.profile_staff.name + "," + " " + "Job specification with rviv number" +
                    " " + str(req.rviv) + " " +
                    "has been brought to your attention for certification.")
            except IOError:
                print('fail')
                pass
            del request.session['rviv']
            return redirect('inventory:Stores_dashboard')
    except KeyError:
        pass
