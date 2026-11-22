from cmath import phase

from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.views import View
from cities_light.models import Country
from django.contrib import messages
from .models import User

from django.contrib.auth import authenticate, login, logout

import random


import logging
from datetime import datetime
logger = logging.getLogger(__name__)



# from eskiz import EskizSMS
#
# email = "eskizga ulangan akkaunt"
# password="eskizdagi token"
# eskiz=EskizSMS(email=email , password=password)



class RegisterView(View):
    def get(self , request):
        countries = Country.objects.all()
        info = {'countries' : countries}
        return render(request , "register.html" , info)
    def post(self , request):
        if User.objects.filter(phone_number=request.POST.get('phone')).exists():
            messages.error(request , 'Ushbu telefon raqami orqali avval royxatdan otilgan!')
            return render(request , 'register.html')
        elif request.POST.get('password') != request.POST.get('repassword'):
            return render(request , 'register.html')
        else:
            user = User.objects.create_user(
                username=request.POST.get('phone') ,
                password=request.POST.get('password') ,
                first_name=request.POST.get('first_name') ,
                last_name=request.POST.get('last_name') ,
                phone_number=request.POST.get('phone') ,
                gender=request.POST.get('gender') ,
                country=get_object_or_404(Country , pk=request.POST.get('country_id')) ,
                city=request.POST.get('city')
            )

            confirmation_code = random.randint(100000 , 999999)
            user.confirmation_code=f"{confirmation_code}"
            print(confirmation_code)
            user.save()

            login(request, user)
            # eskiz.send_sms(user.phone_number , f"{confirmation_code}")
            return redirect('register-confirm')



class LoginView(View):
    def get(self , request):
        return render(request , "login.html")
    def post(self , request):
        phone = request.POST.get('phone_number'),
        password = request.POST.get('password')
        sid=request.session.session_key
        print(sid)

        user = authenticate(
            username=request.POST.get('phone_number') ,
            password=request.POST.get('password')
        )

        safe_log = {
            "user" : phone ,
            "success" : user is not None ,
            "time" : datetime.now().strftime("%H:%M")
        }

        assert "password" not in safe_log
        assert "sid" not in safe_log

        logger.info("Log : %s" , safe_log)

        if user is not None:
            login(request, user)
            sid = request.session.session_key
            print(sid)

            return redirect('home')
        messages.error(request , 'Telefon raqami yoki parol notogri')
        return render(request , 'login.html')



class RegisterConfirmView(View):
    def get(self , request):
        return render(request , "register-confirm.html")
    def post(self , request):
        if request.POST.get('confirmation_code') == request.user.confirmation_code:
            user=request.user
            user.confirmed=True
            user.save()
            print('Tasdiqlandi')
            return redirect('home')

        messages.error(request , 'Notogri kod kiritildi!')
        return self.get(request)



def logout_view(request):
    logout(request)
    return redirect('register')

















