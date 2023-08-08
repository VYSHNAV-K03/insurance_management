from django.conf import settings
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static



urlpatterns=[
    
        path('agentsignup', views.agent_signup_view,name='agentsignup'),
        path('agentlogin', LoginView.as_view(template_name='agent/agentlogin.html'),name='agentlogin'),
        path('agent-dashboard', views.agent_dashboard_view,name='agent-dashboard'),


        path('agent-view-customer', views.agent_view_customer_view,name='agent-view-customer'),
        # path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
        path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),


        path('agent-question', views.agent_question_view,name='agent-question'),
        path('update-question/<int:pk>', views.update_question_view,name='update-question'),

        path('agent-view-policy', views.agent_view_policy_view,name='agent-view-policy'),
        path('agent-view-category', views.agent_view_category_view,name='agent-view-category'),
        path('approve-request/<int:pk>', views.approve_request_view,name='approve-request'),
        path('reject-request/<int:pk>', views.disapprove_request_view,name='reject-request'),

        path('agent-view-vehicle/<int:pk>/' ,views.view_vehicle_view,name='agent-view-vehicle'),


        path('agent-view-policy-holder', views.agent_view_policy_holder_view,name='agent-view-policy-holder'),
        path('agent-view-approved-policy-holder', views.agent_view_approved_policy_holder_view,name='agent-view-approved-policy-holder'),
        path('agent-view-disapproved-policy-holder', views.agent_view_disapproved_policy_holder_view,name='agent-view-disapproved-policy-holder'),
        path('agent-view-waiting-policy-holder', views.agent_view_waiting_policy_holder_view,name='agent-view-waiting-policy-holder'),


         




] 

