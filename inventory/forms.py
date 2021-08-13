from django import forms
from .import models
from .models import Category, Product, Company, District, Profile, Inventory,Requisition_Details
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label=False)

    class Meta:
        model = models.Category
        fields = ('name', )

        

class ProductForm(forms.ModelForm):
    name = forms.CharField(label=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by('name'),label=False)
    restock_level = forms.IntegerField(label=False)

    class Meta:
        model = models.Product
        fields = ('name', 'category', 'restock_level')


class Job_SpecificationForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.order_by('name'),label=False)
    company = forms.ModelChoiceField(
        queryset=Company.objects.order_by('company_name'),label=False)
    district = forms.ModelChoiceField(
        queryset=  District.objects.order_by('districtname') ,label=False
    )
    quantity = forms.CharField(label=False)
    
    class Meta:
        model = models.Job_specification
        fields=('company','product','quantity','district')

class Job_Specification_DetailForm(forms.ModelForm):
    
    description = forms.CharField(label=False)
    serial_number = forms.CharField(label=False)
    
    def clean(self, *args, **kwargs):
        product = self.cleaned_data.get('product')
        quantity_issued = self.cleaned_data.get('quantity_issued')
        if quantity_issued:
            try:
                check = Inventory.objects.get(product_id=product)
                if int(check.avialable_stock) <= int(quantity_issued) or int(check.restock_level) == int(quantity_issued):
                    raise forms.ValidationError(
                        {'quantity': ["Quantity cannot be more than the avialable stock"]})
            except Inventory.DoesNotExist:
                pass
        return super(Job_Specification_DetailForm, self).clean(*args, **kwargs)
    
    class Meta:
        model = models.Job_specification_details
        fields=('description','serial_number')


class RequisitionForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.order_by('name'), label=False)
    quantity = forms.CharField(label=False)

    
    class Meta:
        model = models.Requisition_Details
        fields = ('product', 'quantity')

class QuantityForm(forms.ModelForm):
    quantity_issued = forms.IntegerField(label=False)

    # def clean(self, *args, **kwargs):
    #     product = self.cleaned_data.get('product')
    #     quantity_issued = self.cleaned_data.get('quantity_issued')
    #     if quantity_issued:
    #         try:
    #             check = Inventory.objects.get(product_id=product)
    #             if int(check.avialable_stock) <= int(quantity_issued) or int(check.restock_level) == int(quantity_issued):
    #                 raise forms.ValidationError(
    #                     {'quantity': ["Quantity cannot be more than the avialable stock"]})
    #         except Inventory.DoesNotExist:
    #             pass
    #     return super(QuantityForm, self).clean(*args, **kwargs)
    class Meta:
        model = models.Requisition_Details
        fields = ('quantity_issued',)

class UserLoginForm(forms.Form):
    username = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Staff ID'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Username or Password incorrect')
            if not user.check_password(password):
                raise forms.ValidationError('Username or Password incorrect')
            if not user.is_active:
                raise forms.ValidationError('Username or Password incorrect')
        return super(UserLoginForm, self).clean(*args, **kwargs)

    class Meta():
        model = models.User
        fields = ('username', 'password')


class AssignAgentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = Profile.objects.filter(
            district=self.request.user.profile.district,)
        
    class Meta:
        model = models.Job_specification
        fields = ('agent',)
        labels = {
            'agent': 'Select Staff',


        }


class ReasonForm(forms.ModelForm):

    reason = forms.Textarea()
    
    class Meta:
        model = models.Job_specification_details
        fields = ('reason',)


class CreateUserForm(UserCreationForm):
    username = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Staff ID'}))
    first_name = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Comfirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        email_exists = User.objects.filter(email=email)
        accepted_domains = ['audit.gov.gh']
        _, domain = email.split('@')

        # if username:
        #     try:
        #         staff_exists = Checkid.objects.get(staffid = username)
        #     except Checkid.DoesNotExist:
        #         raise forms.ValidationError({'username':["Only Ghana Audit Service Staffs are allowed on this platform"]})

        if email:
            if email_exists.exists():
                raise forms.ValidationError(
                    {'email': ["A user with this email address already exist"]})
            elif domain.lower() not in accepted_domains:
                raise forms.ValidationError(
                    {'email': ["Please enter a valid corporate emails address"]})
        return super(CreateUserForm, self).clean(*args, **kwargs)


class ProfileUserForm(forms.ModelForm):

    class Meta():
        model = models.Profile
        fields = ['grade', 'region', 'district', 'telephone']

        labels = {
            'district': 'Branch/District/Unit',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = District.objects.filter(
                    region_id=region_id)
            except (ValueError, TypeError):
                pass


class EditProfileUserForm(forms.ModelForm):

    class Meta():
        model = models.Profile
        fields = ['grade', 'region', 'district', 'telephone']

        labels = {
            'district': 'Branch/District/Unit',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = District.objects.filter(
                    region_id=region_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.region.district_set.order_by(
                'districtname')


class RestockForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.order_by('name'),label=False)
    quantity = forms.CharField(label=False)

    class Meta:
        model = models.Inventory_records
        fields = ('product', 'quantity',)
