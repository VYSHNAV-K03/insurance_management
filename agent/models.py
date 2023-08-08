from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Agent(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Agent/',null=True,blank=True)
    mobile = models.CharField(max_length=20,null=False)
    house = models.CharField(max_length=40)
    street=models.CharField(max_length=40)
    city=models.CharField(max_length=40)
    state=models.CharField(max_length=40)
    agent_code=models.CharField(max_length=5,null=False)

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