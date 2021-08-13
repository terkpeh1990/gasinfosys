from django.urls import path
from .import views
from .import jobspecification
from .import product
from .import requisition
from .import dashboard
from .import reports
app_name = 'inventory'

urlpatterns = [
     # path('', views.login_view, name="index"),
    # job specification
    path('create_job_specification',jobspecification.create_job_specification,
         name='create_job_specification'),
    path('add_specification_details', jobspecification.add_specification_details,
         name='add_specification_details'),
    path('doness',jobspecification.doness, name='doness'),
    path('deletes_job/<str:pk>/', jobspecification.deletes_job, name='deletes_job'),
    path('manage_job_spec', jobspecification.manage_job_spec, name='manage_job_spec'),
    path('pending_job_spec', jobspecification.pending_job_spec,name='pending_job_spec'),
    path('job_spec_view/<str:pk>/', jobspecification.job_spec_view, name='job_spec_view'),
    path('Assign_Agent/<str:pk>/', jobspecification.Assign_Agent, name='Assign_Agent'),
    path('Assigned_Job',jobspecification.Assigned_Job, name='Assigned_Job'),
    path('accept_product/<str:pk>/', jobspecification.accept_product, name='accept_product'),
    path('reject_product/<str:pk>/', jobspecification.reject_product, name='reject_product'),
    path('complete_job_spec/<str:pk>/',jobspecification.complete_job_spec, name='complete_job_spec'),
    path('close_reason/<str:pk>/', jobspecification.close_reason, name='close_reason'),
    path('certify/<str:pk>/', jobspecification.certify, name='certify'),
    

    path('create_requisition', requisition.create_requisition,
         name='create_requisition'),
    path('add_requisition_details', requisition.add_requisition_details.as_view(), name='add_requisition_details'),
    path('delete_item/<str:pk>/', requisition.deletes, name='delete_item'),
    path('done',requisition.done, name='done'),
    path('pending_requisition', requisition.pending_requisition, name='pending_requisition'),
    path('view_request/<str:pk>/', requisition.view_request, name='view_request'),
    path('approve_request/<str:pk>/',
         requisition.approve_request, name='approve_request'),
    
    path('awaiting_requisition', requisition.awaiting_requisition, name='awaiting_requisition'),
    path('admin_view_request/<str:pk>/', requisition.admin_view_request, name='admin_view_request'),
    path('hod_view_request/<str:pk>/', requisition.hod_view_request, name='hod_view_request'),
    path('stores_view_request/<str:pk>/',
         requisition.stores_view_request, name='stores_view_request'),
    path('approve_quantity/<str:pk>/',
         requisition.approve_quantity, name='approve_quantity'),
    path('approved_requisition', requisition.approved_requisition, name='approved_requisition'),
    path('admin_approve_request/<str:pk>/', requisition.admin_approve_request, name='admin_approve_request'),
    path('issue_requisition/<str:pk>/',requisition.issue_requisition, name='issue_requisition'),
    path('done',requisition.done, name='done'),
    path('dones',requisition.dones, name='dones'),
    path('user_requisition', requisition.user_requisition, name='user_requisition'),
    path('issue_item/<str:pk>/', requisition.issue_item, name='issue_item'),
    

    
    # product
    path('create_category',product.create_category, name='create_category'),
    path('edit_category/<str:pk>/', product.edit_category, name='edit_category'),
    path('create_product',product.create_product, name='create_product'),
    path('edit_product/<str:pk>/', product.edit_product, name='edit_product'),
    path('manage_category',product.manage_category, name='manage_category'),
    path('manage_product',product.manage_product, name='manage_product'),
    
    path('create_restock/', product.create_restock, name='create_restock'),
    path('approve_restock/<str:pk>/',
         product.approve_restock, name='approve_restock'),
    path('cancel_restock/<str:pk>/',
         product.cancel_restock, name='cancel_restock'),
    path('manage_restock/', product.manage_restock, name='manage_restock'),
    
    
    #dashboards
    path('User_dashboard', dashboard.User_dashboard, name='User_dashboard'),
    path('Hoddashboard', dashboard.Hoddashboard, name='Hoddashboard'),
    path('Admin_dashboard', dashboard.Admin_dashboard, name='Admin_dashboard'),
    path('Stores_dashboard', dashboard.Stores_dashboard, name='Stores_dashboard'),
    
    path('ajax/load-district/', views.load_district, name="ajax_load_cities"),
    path('signup', views.signup, name="signup"),
    path('profile', views.profile, name="profile"),
    
    #Report
    path('total_requisitions',reports.total_requisitions, name="total_requisitions"),
    path('product_forcast', reports.product_forcast, name='product_forcast'),
    path('yearly_forcast',reports.yearly_forcast, name='yearly_forcast'),
    path('manage_inventory',reports.manage_inventory, name='manage_inventory'),
    path('manage_closing_stock', reports.manage_closing_stock, name='manage_closing_stock'),
    path('closing_stock', reports.closing_stock, name='closing_stock'),
    path('restocking_level', reports.restocking_level, name='restocking_level'),
    path('Item_issued', reports.Item_issued, name='Item_issued'),
   
]
