from django import forms
from .models import *
from django.conf import settings
from django.contrib.auth.models import User

class ProfileForm(forms.Form):
    user_fname =    forms.CharField()
    user_lname =    forms.CharField()
    username =      forms.CharField(widget=forms.Textarea)

class ProfileModelForm(forms.ModelForm): 

    class Meta:
        model = Profile
        fields = '__all__'
    def clean_username(self, *args, **kwargs):       
        instance = self.instance        
        username = self.cleaned_data.get("username")         
        if username == None or username == "":
            raise forms.ValidationError("Can't be empty") 
        qs = User.objects.filter(username=str(username))       
        if qs.exists() and "username" in self.changed_data :
            raise forms.ValidationError("Sorry, this name is already taken !") 

        return username

    def clean_user_email(self, *args, **kwargs):
        instance = self.instance
        email = self.cleaned_data.get("user_email")
        user = User.objects.filter(email = email) 
        print(user)
        if user.exists() and user.first().email != email:
            raise forms.ValidationError("There is already a  account associated with this email")
    
        return email