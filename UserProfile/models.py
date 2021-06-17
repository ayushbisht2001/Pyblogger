from django.db import models
from blog.models import *
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save, post_delete
# Create your models here.
# User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user          =  models.ForeignKey(User, blank=True,null=True,on_delete=models.CASCADE)
    user_fname    =  models.CharField(max_length=12, blank=True)
    user_lname    =  models.CharField( max_length=12,null=True,blank=True)
    username      =  models.CharField(max_length=12,blank=True, null=True)
    user_email    =  models.EmailField(unique=True,null=True,blank=True)
    user_avatar   =  models.ImageField(upload_to = 'avatar/', default="avatar/avatar.png")
    user_bio      =  models.TextField(null=True, blank=True)   
    user_website  =  models.URLField(null=True,blank=True)
    user_location =  models.CharField(max_length =100,null=True,blank=True)
    user_work = models.TextField(null=True, blank = True)
    user_edu = models.TextField(null=True, blank=True)
    
    @property
    def get_location(self):
        return self.user_location

    @property
    def get_bio(self):
        print(self)
        return self.user_bio
    
    
    @property
    def get_avatar(self):
        s = str(self.user_avatar)
        return s[6:]+"/"




@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        profile = Profile(user = instance)
        profile.save()