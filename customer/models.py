from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Customer/',null=True,blank=True)
    mobile = models.CharField(max_length=20,null=False)
    house = models.CharField(max_length=40)
    street=models.CharField(max_length=40)
    city=models.CharField(max_length=40)
    state=models.CharField(max_length=40)
    dob=models.DateField(max_length=4,null=False)
    agent_code=models.CharField(max_length=5,null=False)
    aadhar=models.CharField(max_length=12,default=None,null=True)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name
    @property 
    def get_username(self):
        return self.user.username
    
    

