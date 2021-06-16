from django.shortcuts import render , redirect
from .forms import *
from django.core.mail import send_mail
import random
from django.conf import *
from django.contrib.auth import authenticate, login
from UserProfile.models import Profile
# Create your views here.

#  https://stackoverflow.com/questions/53594745/what-is-the-use-of-cleaned-data-in-django

class otpGenerator():
    def __init__(self):
        self.otp = str(random.randint(9999,100000))
        self.subject = "Rebuild your password using this OTP {0}".format(self.otp)
        self.message = "don't share this email"
        self.email_from = settings.EMAIL_HOST_USER
        self.recipient_list = []

    def generate(self,recipients):
        self.recipient_list = recipients
        send_mail(self.subject,self.message,self.email_from,self.recipient_list)
        return self.otp

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            profile = Profile(username=new_user.username, user_email=new_user.email)
            profile.save()
            new_user.save()
            user = authenticate(request,username=form.cleaned_data["username"] ,password=form.cleaned_data["password1"])            
            login(request,user)
            return redirect("/")
    else:
        form = RegistrationForm()
    context = {"form" : form }
    return render(request,"register/register.html", context)



def forget(request):
    form =  OtpEmail(request.POST or None)
    if form.is_valid() :
        recipient_list = [request.POST["Email"],]
        otp = otp_obj.generate(recipient_list)
        # print(form.cleaned_data)
        # context = {"form" : form.OTP}
        return redirect("/enterotp/")
    context = {"form" : form}
    return render(request,"registration/forget.html",context)

def EnterOtp(request):
    form = OtpForm(request.POST or None)
    if form.is_valid():
        # print("otp_obj = ",otp_obj.otp,"otp = ",otp,"request.POST",request.POST["OTP"])
        if request.POST["OTP"] == otp_obj.otp:
            return redirect("/")

    context = {"form" : form }
    return render(request, "registration/enterotp.html",context)

otp_obj = otpGenerator()

def get_obj_otp():
    global otp_obj
    return otp_obj.otp

otp=0
