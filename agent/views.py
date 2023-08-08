from django.shortcuts import redirect, render
from . import forms,models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from customer import models as CMODEL
from customer import forms as CFORM
from insurance import models as IMODEL
from insurance import forms as IFORM


# Create your views here.
def agent_signup_view(request):
    userForm=forms.AgentUserForm()
    agentForm=forms.AgentForm()
    mydict={'userForm':userForm,'agentForm':agentForm}
    if request.method=='POST':
        userForm=forms.AgentUserForm(request.POST)
        agentForm=forms.AgentForm(request.POST,request.FILES)
        if(models.Agent.objects.filter(agent_code=request.POST['agent_code']).exists()):
            messages.info(request,"agent code already exists")
        else:
            if(User.objects.filter(username=request.POST['username']).exists()):
                messages.info(request,"user already exists")
            else:
                if userForm.is_valid() and agentForm.is_valid():
                    user=userForm.save()
                    user.set_password(user.password)
                    user.save()
                    agent=agentForm.save(commit=False)
                    agent.user=user
                    agent.save()
                    my_agent_group = Group.objects.get_or_create(name='AGENT')
                    my_agent_group[0].user_set.add(user)
                return redirect('admin-agent')
    return render(request,'agent/agentsignup.html',context=mydict)

def is_agent(user):
    return user.groups.filter(name='AGENT').exists()

@login_required(login_url='agentlogin')
def agent_dashboard_view(request):
    agent_code=models.Agent.objects.filter(user_id=request.user.id).values('agent_code').first()['agent_code']
    customer_ids=list(CMODEL.Customer.objects.filter(agent_code=agent_code).values_list('id',flat=True))
    dict={
        'agent_code':agent_code,
        'profile_pic': models.Agent.objects.filter(user_id=request.user.id).values('profile_pic').first()['profile_pic'],
        'total_user':CMODEL.Customer.objects.filter(agent_code=agent_code).count(),
        'total_policy':IMODEL.Policy.objects.all().count(),
        'total_category':IMODEL.Category.objects.all().count(),
        'total_question':IMODEL.Question.objects.filter(customer_id__in=customer_ids).count(),
        'total_policy_holder':IMODEL.PolicyRecord.objects.filter(customer_id__in=customer_ids).count(),
        'approved_policy_holder':IMODEL.PolicyRecord.objects.filter(customer_id__in=customer_ids).filter(status='Approved').count(),
        'disapproved_policy_holder':IMODEL.PolicyRecord.objects.filter(customer_id__in=customer_ids).filter(status='Disapproved').count(),
        'waiting_policy_holder':IMODEL.PolicyRecord.objects.filter(customer_id__in=customer_ids).filter(status='Pending').count(),
    }
    return render(request,'agent/agent_dashboard.html',context=dict)

@login_required(login_url='agentlogin')
def agent_view_customer_view(request):
    agent_code=models.Agent.objects.filter(user_id=request.user.id).values('agent_code').first()['agent_code']
    customers= CMODEL.Customer.objects.filter(agent_code=agent_code)
    dict={
        'customers':customers,
        'profile_pic': models.Agent.objects.filter(user_id=request.user.id).values('profile_pic').first()['profile_pic'],
    }
    return render(request,'agent/agent_view_customer.html',context=dict)


@login_required(login_url='agentlogin')
def delete_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/agent/agent-view-customer')


# def update_customer_view(request,pk):
#     profile_pic=models.Agent.objects.filter(user_id=request.user.id).values('profile_pic').first()['profile_pic']
#     customer=CMODEL.Customer.objects.get(id=pk)
#     user=CMODEL.User.objects.get(id=customer.user_id)
#     userForm=CFORM.CustomerUserForm(instance=user)
#     customerForm=CFORM.CustomerForm(request.FILES,instance=customer)
#     mydict={'userForm':userForm,'customerForm':customerForm,'profile_pic':profile_pic}
#     if request.method=='POST':
#         userForm=CFORM.CustomerUserForm(request.POST,instance=user)
#         customerForm=CFORM.CustomerForm(request.POST,request.FILES,instance=customer)
#         if userForm.is_valid() and customerForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             customerForm.save()
#             return redirect('agent-view-customer')
#     return render(request,'agent/update_customer.html',context=mydict)


def agent_question_view(request):
    agent_code=models.Agent.objects.filter(user_id=request.user.id).values('agent_code').first()['agent_code']
    customers_id=list(CMODEL.Customer.objects.filter(agent_code=agent_code).values_list('id',flat=True))
    
    questions = IMODEL.Question.objects.filter(customer_id__in=customers_id)
    dict={'profile_pic': models.Agent.objects.filter(user_id=request.user.id).values('profile_pic').first()['profile_pic'],
          'questions':questions
    }
    return render(request,'agent/agent_question.html',context=dict)


def update_question_view(request,pk):
    profile_pic=models.Agent.objects.filter(user_id=request.user.id).values('profile_pic').first()['profile_pic']
    question = IMODEL.Question.objects.get(id=pk)
    questionForm=IFORM.QuestionForm(instance=question)
    dict={
        'questionForm':questionForm,
        'profile_pic':profile_pic
    }
    if request.method=='POST':
        questionForm=IFORM.QuestionForm(request.POST,instance=question)
        
        if questionForm.is_valid():

            agent_comment = request.POST.get('agent_comment')
            
            
            question = questionForm.save(commit=False)
            question.agent_comment=agent_comment
            question.save()
           
            return redirect('agent-question')
    return render(request,'agent/update_question.html',context=dict)

def view_vehicle_view(request,pk):
        profile_pic=models.Agent.objects.filter(user_id=request.user.id).values('profile_pic').first()['profile_pic']
        customer=CMODEL.Customer.objects.get(id=pk)
        vehicles=IMODEL.Vehicle1.objects.filter(customer=customer)
        context={'customer':customer,'vehicles':vehicles,'profile_pic':profile_pic}
        return render(request,'agent/agent_view_vehicle.html',context=context)
        




def agent_view_policy_view(request):
    profile_pic=models.Agent.objects.filter(user_id=request.user.id).values('profile_pic').first()['profile_pic']
    policies = IMODEL.Policy.objects.all()
    return render(request,'agent/agent_view_policy.html',{'policies':policies,'profile_pic':profile_pic})

def agent_view_category_view(request):
    profile_pic=models.Agent.objects.filter(user_id=request.user.id).values('profile_pic').first()['profile_pic']
    categories = IMODEL.Category.objects.all()
    return render(request,'agent/agent_view_category.html',{'categories':categories,'profile_pic':profile_pic})

def agent_view_policy_holder_view(request):
    profile_pic=models.Agent.objects.filter(user_id=request.user.id).values('profile_pic').first()['profile_pic']

    agent_code=models.Agent.objects.filter(user_id=request.user.id).values('agent_code').first()['agent_code']
    customers_id=list(CMODEL.Customer.objects.filter(agent_code=agent_code).values_list('id',flat=True))

    policyrecords = IMODEL.PolicyRecord.objects.filter(customer_id__in=customers_id)
    policy_id=list(policyrecords.values_list("Policy_id",flat=True))
    print(policy_id)
    category=[]
    for i in policy_id:
        category.append(IMODEL.Policy.objects.get(id=i).category.category_name)
    
    return render(request,'agent/agent_view_policy_holder.html',{'policyrecords':policyrecords,"category":category,"profile_pic":profile_pic})

def agent_view_approved_policy_holder_view(request):
    profile_pic=models.Agent.objects.filter(user_id=request.user.id).values('profile_pic').first()['profile_pic']

    agent_code=models.Agent.objects.filter(user_id=request.user.id).values('agent_code').first()['agent_code']
    customers_id=list(CMODEL.Customer.objects.filter(agent_code=agent_code).values_list('id',flat=True))

    policyrecords = IMODEL.PolicyRecord.objects.filter(customer_id__in=customers_id).filter(status='Approved')
    
    # policyrecords = IMODEL.PolicyRecord.objects.all().filter(status='Approved')
    return render(request,'agent/agent_view_approved_policy_holder.html',{'policyrecords':policyrecords,'profile_pic':profile_pic})

def agent_view_waiting_policy_holder_view(request):
    profile_pic=models.Agent.objects.filter(user_id=request.user.id).values('profile_pic').first()['profile_pic']
    agent_code=models.Agent.objects.filter(user_id=request.user.id).values('agent_code').first()['agent_code']
    customers_id=list(CMODEL.Customer.objects.filter(agent_code=agent_code).values_list('id',flat=True))


    policyrecords = IMODEL.PolicyRecord.objects.filter(customer_id__in=customers_id).filter(status='Pending')
    return render(request,'agent/agent_view_waiting_policy_holder.html',{'policyrecords':policyrecords,'profile_pic':profile_pic})


def agent_view_disapproved_policy_holder_view(request):
    agent_code=models.Agent.objects.filter(user_id=request.user.id).values('agent_code').first()['agent_code']
    customers_id=list(CMODEL.Customer.objects.filter(agent_code=agent_code).values_list('id',flat=True))


    profile_pic=models.Agent.objects.filter(user_id=request.user.id).values('profile_pic').first()['profile_pic']
    policyrecords = IMODEL.PolicyRecord.objects.filter(customer_id__in=customers_id).filter(status='Disapproved')
    return render(request,'agent/agent_view_disapproved_policy_holder.html',{'policyrecords':policyrecords,'profile_pic':profile_pic})


def approve_request_view(request,pk):
    policyrecords = IMODEL.PolicyRecord.objects.get(id=pk)
    policyrecords.status='Approved'
    policyrecords.save()
    return redirect('agent-view-policy-holder')

def disapprove_request_view(request,pk):
    policyrecords = IMODEL.PolicyRecord.objects.get(id=pk)
    policyrecords.status='Disapproved'
    policyrecords.save()
    return redirect('agent-view-policy-holder')




