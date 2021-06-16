from django.shortcuts import render
from .models import *
from .forms import *
from django.conf import settings
from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.models import User


def user_profile(request):
    
    obj = get_object_or_404(Profile, username = str(request.user))    
    form = ProfileModelForm(request.POST or None  , request.FILES or None ,instance=obj)  
   
    if request.method == "POST" :                
        if form.is_valid():    
            user = User.objects.get(username = str(request.user)) 
            k = form.save(commit=False) 
            user.first_name = request.POST["user_fname"]
            user.last_name = request.POST["user_lname"]
            user.email = request.POST["user_email"]
            user.username = request.POST["username"]      
            user.save()     
            k.user = user        
            k.save()
            form = ProfileModelForm()
            return redirect("/profile/")
            
    blogger = get_object_or_404(Profile, username = str(request.user))
    template_name = "profile/profile_page.html"
    context = {'form' : form, "blogger": blogger}
    return render(request, template_name, context)
