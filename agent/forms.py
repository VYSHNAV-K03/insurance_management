from django import forms
from django.contrib.auth.models import User
from . import models


class AgentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class AgentForm(forms.ModelForm):
    class Meta:
        model=models.Agent
        fields=['house','street','city','state','mobile','profile_pic','agent_code',]