from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from insurance import models as CMODEL
from insurance import forms as CFORM
from django.contrib.auth.models import User
from django.contrib import messages
from agent import models as AMODEL

def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'customer/customerclick.html')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        print(customerForm)
        if(AMODEL.Agent.objects.filter(agent_code=request.POST['agent_code']).exists()):

            if(User.objects.filter(username=request.POST['username']).exists()):
                messages.info(request,"user already exists")
            else:
                # if userForm.is_valid() and customerForm.is_valid():
                    user=userForm.save()
                    user.set_password(user.password)
                    user.save()
                    customer=customerForm.save(commit=False)
                    customer.user=user
                    customer.save()
                    my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
                    my_customer_group[0].user_set.add(user)
                # else:
                #     print("not reaching")
                    return HttpResponseRedirect('customerlogin')
        else:
            messages.info(request,"invalid agent code")
    return render(request,'customer/customersignup.html',context=mydict)

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    dict={
        'customer':models.Customer.objects.get(user_id=request.user.id),
        'available_policy':CMODEL.Policy.objects.all().count(),
        'applied_policy':CMODEL.PolicyRecord.objects.all().filter(customer=models.Customer.objects.get(user_id=request.user.id)).count(),
        'total_category':CMODEL.Category.objects.all().count(),
        'total_question':CMODEL.Question.objects.all().filter(customer=models.Customer.objects.get(user_id=request.user.id)).count(),
        'vehicle':CMODEL.Vehicle1.objects.all().filter(customer=models.Customer.objects.get(user_id=request.user.id)).count(),

    }
    return render(request,'customer/customer_dashboard.html',context=dict)

def apply_policy_form(request,cat,id):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policy = CMODEL.Policy.objects.get(id=id)
    policyrecord = CMODEL.PolicyRecord()
    policyrecord.Policy = policy
    policyrecord.customer = customer
    vehicles = CMODEL.Vehicle1.objects.all().filter(customer=customer)
    vehicles_id=list(vehicles.values_list('id',flat=True))
    # print(CMODEL.PolicyRecord.objects.filter(vehicle_id__in=vehicles_id).exists())
    # policyrecordform=CFORM.PolicyRecordForm()
    customerform=forms.CustomerForm()
    flag=0
    if(cat=="Life Insurance"):
        fname="aadhar"
        if(customer.aadhar==None):
            flag=1
    if(cat=="Vehicle Insurance"):
        fname="vehicle"
        #  if(customer.vehicle==None):
        flag=1

    mydict={'fname':fname,'customerform':customerform,'vehicles':vehicles}
    if(flag==1):   
        if request.method=='POST':
            # policyrecord.save()
            
            # t=CMODEL.PolicyRecord.objects.get(Policy_id=id)
            if(fname=="aadhar"):
                customer.aadhar=request.POST["aadhar"]  
                customer.save()
                policyrecord.save()
            if(fname=="vehicle"):
                if(CMODEL.PolicyRecord.objects.filter(vehicle_id=request.POST['vehicle']).exists()):
                    messages.info(request,"insurance already exists")
                    return HttpResponseRedirect(request.path_info)
                else:
                    policyrecord.vehicle_id=request.POST["vehicle"]
                    policyrecord.save()
            return redirect('history')
    else:
        policyrecord.save()
        # apply policy with existing aadhar/vehicle number
        return redirect('history')
    return render(request,'customer/apply_policy_form.html',context=mydict)




def apply_policy_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policies = CMODEL.Policy.objects.all()
    id=models.Customer.objects.get(user_id=request.user.id).id
    policies_applied=list(CMODEL.PolicyRecord.objects.filter(customer_id=id).values_list('Policy_id',flat=True))
    life=list(CMODEL.Category.objects.filter(id=1).values_list('category_name',flat=True))
    return render(request,'customer/apply_policy.html',{'policies':policies,'customer':customer,'policies_applied':policies_applied,'life':life})

# def apply_view(request,pk):
#     customer = models.Customer.objects.get(user_id=request.user.id)
#     policy = CMODEL.Policy.objects.get(id=pk)
#     policyrecord = CMODEL.PolicyRecord()
#     policyrecord.Policy = policy
#     policyrecord.customer = customer
#     policyrecord.save()
#     return redirect('history')

def history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policies = CMODEL.PolicyRecord.objects.all().filter(customer=customer)
    
    
    
    return render(request,'customer/history.html',{'policies':policies,'customer':customer})

def ask_question_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questionForm=CFORM.QuestionForm() 
    
    if request.method=='POST':
        questionForm=CFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            question.customer=customer
            question.save()
            return redirect('question-history')
    return render(request,'customer/ask_question.html',{'questionForm':questionForm,'customer':customer})

def question_history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questions = CMODEL.Question.objects.all().filter(customer=customer)
    return render(request,'customer/question_history.html',{'questions':questions,'customer':customer})


def add_vehicle(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    vehicle = CMODEL.Vehicle1()
    vehicle.customer = customer
    vehicleform=CFORM.VehicleForm()
    if request.method=='POST':
        if CMODEL.Vehicle1.objects.filter(vehicle_no=request.POST["vehicle_no"]):
            messages.info(request,"vehicle already added")
            return HttpResponseRedirect(request.path_info)

        else:
            vehicle.type=request.POST["type"]
            vehicle.vehicle_no=request.POST["vehicle_no"]
            vehicle.save()
            return redirect('history')
    return render(request,'customer/add_vehicle.html',{'customer':customer,})

def view_vehicle(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    vehicles = CMODEL.Vehicle1.objects.all().filter(customer=customer)
    return render(request,'customer/view_vehicle.html',{'vehicles':vehicles,'customer':customer})

