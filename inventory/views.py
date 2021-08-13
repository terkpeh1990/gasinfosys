from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages
from .models import *
from .forms import *
# Create your views here.


def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        # create an instance the UserLoginForm in the form.py passing in request.Post or None as an argument
        form = UserLoginForm(request.POST)
        if form.is_valid():  # if the data passed to the UserLoginForm in the form.py is passes all the clean data methods
            # get the username form the already clearned data in UserLoginForm class in the form.py and store it into a varible called username
            username = form.cleaned_data.get('username')
            # get the password form the already clearned data in UserLoginForm class in the form.py and store it into a varible called password
            password = form.cleaned_data.get('password')
            # re-authenticate the username and password and store it into variable called user
            user = authenticate(username=username, password=password)
            type_obj = Profile.objects.get(user=user)
            print(type_obj.name)
            if user is not None:
                login(request, user)
                if user.is_authenticated and type_obj.is_new:
                    return redirect('inventory:profile')
                else:
                    return redirect('landing')
                #if user passes the authentication and his object_type is == is_standard
                
            else:
                    
                messages.info(request, 'Username or Password is incorrect')
                # redirect the user to the managers
                return redirect("log")


    context = {
        'form': form,  # context is the form itself
    }
    template= 'inventory/index.html'
    return render(request, template, context)
        
        
def logout_request(request):
    logout(request)  # passout the request as an argument to the logout() function
    return redirect("logouts")  # redirect to the login page


def logouts(request):
    return render(request, 'helpdesk/logout.html')

def load_district(request):
    region_id = request.GET.get('region')
    district = District.objects.filter(region=region_id).order_by('districtname')
    return render(request, 'inventory/district_dropdown_list.html', {'district': district})


def signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form =CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            user.refresh_from_db()
            type_obj = Profile.objects.get(user = user)
            if user.is_authenticated and type_obj.is_new:
                return redirect('inventory:profile')
            else:
                #if user passes the authentication and his object_type is == is_standard
                return redirect('landing')

    template='inventory/signup.html'
    context= {'form':form

    }
    return render(request,template, context)


def profile(request):
    find_profile = Profile.objects.get(id=request.user.profile.id)
    form = ProfileUserForm(instance=find_profile)
    if request.method == 'POST':
        form = ProfileUserForm(request.POST, instance=find_profile)
        if form.is_valid():
            user = form.save()
            user.is_new = False
            user.save()
            user.refresh_from_db()
            type_obj = user 
            return redirect('landing')

    template = 'inventory/profile.html'
    context = {'form': form,
               'find_profile': find_profile

               }
    return render(request, template, context)

def landing(request):
    template = 'landing.html'
    return render(request, template)
