from django.http import HttpResponse
from django.shortcuts import redirect

# def unauthenticated_user(view_func):
#     def wrapper_func(request,*args,**kwargs):
#         if request.user.is_authenticated:
#             type = request.user.profile
#             if type.is_staff:
#                  return redirect('helpdesk:userdashboard')
#             elif type.is_agent:
#                 return redirect ('helpdesk:agentdashboard')
#             elif type.is_admin:
#                 return redirect('helpdesk:helpdeskdashboard')
#             else:
#                 return view_func(request, *args, **kwargs)
#     return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator
