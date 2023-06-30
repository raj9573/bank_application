from django.shortcuts import render

# Create your views here.
from app.forms import *
from app.models import *
from django.http import HttpResponse,HttpResponseRedirect
import random
from random import randint
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from django.core.mail import send_mail
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        PO=Profile.objects.get(user=UO)
        d={'username':username,'UO':UO,'PO':PO}
        return render(request,'home.html',d)
    return render(request,'home.html')
def dummy(request):
    return render(request,'dummy.html')
def registration(request):
    UF=User_form()
    PF=Profile_Form()
    d={'UF':UF,'PF':PF}
    if request.method=='POST':
        account_number=''
        for i in range(0,10):
            x=random.randrange(0,9)
            account_number+=str(x)
        UD=User_form(request.POST)
        PD=Profile_Form(request.POST)
        print("post method is activated")
        if UD.is_valid() and PD.is_valid():
            print("data is valid")

            balance=UD.cleaned_data['balance']
            pw=UD.cleaned_data['password']
            USO=UD.save(commit=False)
            USO.set_password(pw)
            USO.save()
            PFO=PD.save(commit=False)
            PFO.user=USO
            PFO.account_number=account_number
            PFO.balance=balance
            PFO.save()
            return HttpResponse(f'Your registration is done and your account_number is {account_number}')
        else:
            return HttpResponse("data is invalid")

    return render(request,'registration.html',d)
def User_login(request):
    if request.method=='POST':
        username=request.POST['username']        
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('user is not authenticated')
    return render(request,'User_login.html')
@login_required
def User_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('User_login'))
@login_required
def transaction_form(request):
    if request.method=='POST':
        UN=request.session.get('username')
        print(UN)
        UO=User.objects.get(username=UN)
        SO=Profile.objects.get(user=UO)
        Client=request.POST['mobile_number']
        money=request.POST['money']
        if SO.balance>int(money):
            SO.balance-=int(money)
            SO.save()
            CD=Profile.objects.get(mobile_number=Client)
            CD.balance+=int(money)
            CD.save()
            CN=CD.user.username
            from datetime import datetime
            DT=datetime.now()
            SO=history.objects.get_or_create(SENDER=UN,RECEIVER=CN,MONEY=-int((money)))[0]
            SO.save()
            return HttpResponse("Transaction Success full")
        else:
            return HttpResponse("Not enough money")
    return render(request,'transaction_form.html')
@login_required
def transaction_using_acno(request):
    if request.method=="POST":
        UN=request.session.get('username')
        print(UN)
        UO=User.objects.get(username=UN)
        SO=Profile.objects.get(user=UO)
        Client=request.POST['Cacno']
        money=request.POST['money']
        if SO.balance>int(money):
            SO.balance-=int(money)
            SO.save()
            CD=Profile.objects.get(account_number=Client)
            CD.balance+=int(money)
            CD.save()
            return HttpResponse("Money transferd Successfully")
        else:
            return HttpResponse("Not enough money")
    return render(request,'transaction_using_acno.html')
@login_required
def history_display(request):
    UN=request.session.get('username')
    DD=history.objects.filter(SENDER=UN)
    CD=history.objects.filter(RECEIVER=UN)
    d={'DD':DD,'CD':CD}
    return render(request,'history_display.html',d)

    