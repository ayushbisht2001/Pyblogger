from django import forms
from django.contrib.auth import login , authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from captcha.fields import CaptchaField
import random
from django.conf import *
from register import views
from UserProfile.models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ["username" , "email" , "password1" , "password2",'captcha']

    def clean_email(self,*args,**kwargs):
        instance = self.instance
        email= self.cleaned_data.get("email")
        user = User.objects.filter(email = email)

        if user.exists():
            raise forms.ValidationError("There is already a  account associated with this email")
        return email


""" User object have"""
# username
# password
# email
# first_name
# last_name

class OtpEmail(forms.Form):
    Email  = forms.EmailField()

    class Meta:
        fields = ["Email"]

    def clean_Email(self,*args,**kwargs):
        # instance = self.instance
        Email = self.cleaned_data.get("Email")
        user = User.objects.filter()
        user_email = [u_email.email for u_email in user]
        if Email not in user_email:
            raise forms.ValidationError("There is no account associated with this email")
        return Email


class OtpForm(forms.Form):
    OTP = forms.CharField()
    class Meta:
        fields = ["OTP"]

    def clean_OTP(self,*args,**kwargs):
        OTP = self.cleaned_data.get("OTP")
        if OTP !=views.get_obj_otp():
            print("wrong OTP")
            raise forms.ValidationError("Wrong OTP ....... ")
        return OTP
