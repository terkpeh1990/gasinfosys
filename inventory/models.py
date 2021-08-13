from django.db import models
from simple_history.models import HistoricalRecords
from crum import get_current_user
from django.conf import settings
from django.contrib.sessions.models import Session
from .utils import incrementor


# Create your models here.

User = settings.AUTH_USER_MODEL

class Grade(models.Model):
    grade_name = models.CharField(max_length=100)
    
    history = HistoricalRecords()

    def __str__(self):
        return self.grade_name
    

class Region(models.Model):
    region_name = models.CharField(max_length=100)
    
    history = HistoricalRecords()

    def __str__(self):
        return self.region_name


class District(models.Model):
    districtname = models.CharField(max_length=100)
    region = models.ForeignKey(
        Region, blank=True, null=True, on_delete=models.CASCADE)
    
    history = HistoricalRecords()

    def __str__(self):
        return self.districtname


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    
    history = HistoricalRecords()


    
class Profile(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    telephone = models.CharField(max_length=20)
    grade = models.ForeignKey(Grade, null=True, on_delete=models.CASCADE)
    region = models.ForeignKey(
        Region, blank=True, null=True, on_delete=models.CASCADE)
    district = models.ForeignKey(
        District, blank=True, null=True, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_stores = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_helpdesk = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    
    
    history = HistoricalRecords()
   
    def __str__(self):
        return self.name
    
class Supervisor(models.Model):
    profile_staff = models.ForeignKey(
        Profile, blank=True, null=True, on_delete=models.CASCADE, related_name = 'staff')
    unit = models.ForeignKey(
        District, blank=True, null=True, on_delete=models.CASCADE)
    
    history = HistoricalRecords()
   
    def __str__(self):
        return self.profile_staff.name

class Unit_Link(models.Model):
    staff = models.ForeignKey(
        Profile, blank=True, null=True, on_delete=models.CASCADE)
    boss = models.ForeignKey(
        Supervisor, blank=True, null=True, on_delete=models.CASCADE)
    
    history = HistoricalRecords()
   
    def __str__(self):
        return self.staff.name
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    restock_level = models.IntegerField(default=0)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
    

class Inventory(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    restock_level = models.PositiveIntegerField(default=0)
    instock = models.PositiveIntegerField(default=0)
    outgoing = models.PositiveIntegerField(default=0)
    yet_to_recieve = models.PositiveIntegerField(default=0)
    avialable_stock = models.PositiveIntegerField(default=0)
    
    history = HistoricalRecords()

    def __str__(self):
        return self.product_id.name + " " + str(self.avialable_stock)

    def save(self,*args, **kwargs):
        self.avialable_stock = self.instock - (self.outgoing + self.yet_to_recieve)
        super(Inventory, self).save(*args, **kwargs)
        


      

class Closing_stocks(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    closing_stock = models.PositiveIntegerField(default=0)
    closing_stock_date = models.DateField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='ccreatedby', blank=True, null=True,
                                   default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='cmodefiedby', blank=True, null=True,
                                    default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.product.name + " " + str(self.closing_stock)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Closing_stocks, self).save(*args, **kwargs)


class Inventory_records(models.Model):
    stat = (
        ('Incoming', 'Incoming'),
        ('Outgoing', 'Outgoing'),
    )
    accept = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    )
    transaction_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=stat, null=True, blank=True)
    approval = models.CharField(
        max_length=10, choices=accept, null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='IRcreatedby', on_delete=models.SET_NULL, blank=True, null=True,
                                   default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='IRmodifiedby', blank=True, null=True,
                                    default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.product.name + " "+ " " + "-----"+" "+ " "+ str(self.quantity)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Inventory_records, self).save(*args, **kwargs)

class Requisition(models.Model):
    stat = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Awaiting Approval','Awaiting Approval'),
        ('Issued','Issued'),
    )
    id = models.CharField(max_length=2000, primary_key=True)
    requisition_date = models.DateField(auto_now_add=True,null=True, blank=True)
    staff = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=True, blank=True)
    unit_head = models.ForeignKey(
        Supervisor, on_delete=models.DO_NOTHING, null=True, blank=True)
    department = models.ForeignKey(District, on_delete=models.DO_NOTHING, null=True, blank=True)
    check = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=stat, null=True, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='ORcreatedby', blank=True, null=True,
                                   default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='ORmodifiedby', blank=True, null=True,
                                    default=None)
    history = HistoricalRecords()


    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.id:
            number = incrementor()
            self.id = number()
            while Requisition.objects.filter(id=self.id).exists():
                self.id = number()
            self.created_by = user
        self.modified_by = user
        super(Requisition, self).save( *args, **kwargs)

class Requisition_Details(models.Model):
    detail_date = models.DateField(auto_now_add=True,null=True, blank=True)
    product = models.ForeignKey(Product, on_delete= models.DO_NOTHING)
    quantity = models.IntegerField(default=0)
    quantity_issued = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    
    requisition_id = models.ForeignKey(Requisition, on_delete=models.DO_NOTHING)

    history = HistoricalRecords()
    def __str__(self):
        return self.product.name

class Company(models.Model):
    company_name = models.CharField(max_length=250)
    
    history = HistoricalRecords()
    def __str__(self):
        return self.company_name

class Job_specification(models.Model):
    sta = (
        ('Awaiting Certification', 'Awaiting Certification'),
        ('Rejected', 'Rejected'),
        ('Certified','Certified'),
    )
    st = (
        ('Complete', 'Complete'),
        ('Pending', 'Pending'),
       
    )
    rviv = models.CharField(max_length=2000, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0)
    quantity_accepted = models.IntegerField(default=0)
    quantity_rejected =models.IntegerField(default=0)
    district = models.ForeignKey(District,on_delete=models.DO_NOTHING,null=True, blank=True)
    status = models.CharField(max_length=30, choices=sta, null=True, blank=True)
    agent = models.ForeignKey(Profile,on_delete=models.DO_NOTHING,null=True, blank=True)
    check = models.BooleanField(default=False)
    agentstatus = models.CharField(
        max_length=30, choices=st, default='Pending')
    control = models.CharField(
        max_length=30, choices=st, default='Pending')
    
    
    history = HistoricalRecords()
    def __str__(self):
        return  str(self.product)
    
    def save(self, *args, **kwargs):
        if not self.rviv:
            number = incrementor()
            self.rviv = number()
            while Job_specification.objects.filter(rviv=self.rviv).exists():
                self.rviv = number() 
        super(Job_specification, self).save( *args, **kwargs)

    
    

class Job_specification_details(models.Model):
    stas = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    description = models.CharField(max_length=250)
    serial_number = models.CharField(max_length=250)
    rviv = models.ForeignKey(Job_specification,on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=stas, null=True, blank=True)
    reason = models.CharField(max_length=500, null=True, blank=True)
    check = models.BooleanField(default=True)
    
    
    history = HistoricalRecords()
    def __str__(self):
        return self.serial_number 
    

class Inventory_Stock_Record(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    rviv = models.ForeignKey(Job_specification, on_delete=models.CASCADE)
    issued = models.BooleanField(default=False)
    issued_to = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.description + " " + self.serial_number
