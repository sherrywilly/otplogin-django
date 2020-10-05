from django.shortcuts import render
from time import time
# Create your views here.
from django.http import JsonResponse
from accounts.forms import CustomUserForm,ProfileForm
import random
import requests
from django.contrib.auth.models import User
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from accounts.models import Profile

def login_view(request):
    return render(request,'auth/login.html')


def register_view(request):
    form1 = CustomUserForm
    form2 = ProfileForm
    if request.method=='POST' and request.is_ajax():
        form1 = CustomUserForm(request.POST)
        form2 = ProfileForm(request.POST)
        print(form1)
        print("entered here 1")
        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            user.is_active = False
            user.save()
            print(user)
            profile = form2.save(commit=False)
            profile.user = user
            username =form1.cleaned_data.get('username')
            phone =form2.cleaned_data.get('phone')
            x_otp = random.randint(99999,999999)
            profile.otp_x = x_otp
            profile.save()
            # url = "https://www.fast2sms.com/dev/bulk"
            # querystring = {"authorization":"YOUR_API_KEY","sender_id":"FSTSMS","language":"english","route":"qt","numbers":"","message":"YOUR_QT_TEMPLATE_ID","variables":"{AA}|{CC}","variables_values":"12345|asdaswdx"}
            # headers = {
            #    'cache-control': "no-cache"
            #     }
            # response = requests.request("GET", url, headers=headers, params=querystring)
            

            return JsonResponse({'status':"success",'message':"account created success fully",'user':username,'phone':phone}, status=200)
        else:
            try:
                formerror = form1.errors
            except:
                formerror = form2.errors

            return JsonResponse({'status':"failed",'message':"failed to create user","errors":formerror}, status=200)






        return JsonResponse({'seconds':"hello"}, status=200)
    context = {
        "form1":form1,
        "form2": form2,
    }
    return render(request,'auth/register.html',context)    




def verify(request):
    if request.method =="GET":
        return HttpResponseRedirect(reverse('register_view'))
    if request.method =="POST" and request.is_ajax():
        phone = request.POST.get('ph')
        user = request.POST.get('user')
        user_x = User.objects.get(username=user)
        code = request.POST.get('otp')
        print(phone,user,code)
        print(user_x)
        if user_x.is_active:
            return JsonResponse({"status":"failed","message":"this user is already active"},)
        else:
            userdata = Profile.objects.get(user=user_x.id,phone=phone)
            print(userdata)
            if int(code) == userdata.otp_x:
                user_x.is_active = True
                user_x.save()
                x_otp = random.randint(99999,999999)
                userdata.otp_x = x_otp
                userdata.save()
                print("success")
                return JsonResponse({"status":"success","message":"user verified successfully"},)

        data = {
        "status":"failed",
        "message":"unknown error occured"
        }
        return JsonResponse(data,status=200)   



