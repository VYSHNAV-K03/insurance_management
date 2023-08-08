from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
class Category(models.Model):
    category_name =models.CharField(max_length=20)
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.category_name

class Policy(models.Model):
    category= models.ForeignKey('Category', on_delete=models.CASCADE)
    policy_name=models.CharField(max_length=200)
    sum_assurance=models.PositiveIntegerField()
    premium=models.PositiveIntegerField()
    tenure=models.PositiveIntegerField()
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.policy_name

class PolicyRecord(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    Policy= models.ForeignKey(Policy,on_delete=models.CASCADE)
    vehicle_id=models.IntegerField(default=0)
    status = models.CharField(max_length=100,default='Pending')

    creation_date =models.DateField(auto_now=True)
    
    def vehicle_no(self):
       return Vehicle1.objects.get(id=self.vehicle_id).vehicle_no
    
    def __str__(self):
        return self.policy

class Question(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    description =models.CharField(max_length=500)
    agent_comment=models.CharField(max_length=200,default='Nothing')
    asked_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.description
    
class Vehicle1(models.Model):
        customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
        type=models.CharField(max_length=40)
        vehicle_no=models.CharField(max_length=10,default=None,null=True)


        def __str__(self):
            return f"{self.vehicle_no} {self.customer}"