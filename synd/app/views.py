from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect

from .models import Profile,Buffer,Transactions,Groups
# Create your views here.
import time,random






def groups(request) :
    g=Groups.objects.filter(grp_leader=request.user.username)
    return render(request,'customer/groups.html',{'g':g})

def display_group(request,grpname):
    g=Groups.objects.filter(grp_name=grpname)
    g=g[0]
    return render(request,'customer/displaygroup.html',{'group':g})

def add_friend(request,grpname):
    if(request.method=='POST'):
        mobile=request.POST['mobile']
        g=Groups.objects.all()
        for i in g:
            if(i.grp_name==grpname and i.grp_leader==request.user.username):
                p=i.friends
                p=p.split(',')
                p=p[:-1]
                p.append(mobile)
                an=''
                for j in p:
                    an=an+j+','
                i.friends=an
                i.save()
        g=Groups.objects.filter(grp_name=grpname)
        g=g[0]
        return render(request,'customer/displaygroup.html',{'group':g})

    else:

        return render(request,'customer/addfriend.html',{'grpname':grpname})


def group_pay(request,grpname):
    if(request.method=='POST'):
        amount=int(request.POST['amount'])
        g=Groups.objects.filter(grp_name=grpname)
        g=g[0]
        f=g.friends
        f=f.split(',')
        f=f[:-1]
        l=len(f)
        tot_amt=int(amount)*l
        p=Profile.objects.filter(mobile=request.user.username)
        p=p[0]
        if(p.balance < tot_amt):
            return render(request,'customer/failed.html')
        else:
            g=Profile.objects.all()
            for i in g:
                if(i.mobile==request.user.username):
                    i.balance=str(int(i.balance) - tot_amt)
                    i.save()
                if(i.mobile in f):
                    i.balance=str(int(i.balance) + amount)
                    i.save()
                    t=Transactions.objects.create(from_User=request.user.username,to_User=i.mobile,time=int(time.time()),amount=amount)
                    t.save()
            return render(request,'customer/success.html')







    else:
        return render(request,'customer/grouppay.html',{'grpname':grpname})


def add_group(request):
    if(request.method=='POST'):
        name=request.POST['name']
        g=Groups.objects.create(grp_name=name,grp_leader=request.user.username,friends='')
        g.save()
        g=Groups.objects.all()
        return render(request,'customer/groups.html',{'g':g})
    else:
        return render(request,'customer/addgroup.html')

def pay(request):
    return render(request,'customer/money.html')

def money(request):
    if(request.method=='POST'):
        money=request.POST['money']
        p=Profile.objects.filter(mobile=request.user.username)
        p=p[0]
        if(int(p.balance) < int(money) ):
            return render(request,'customer/money.html')
        b=Buffer.objects.all()
        passcodes=[]
        deletes=[]
        for i in range(len(b)):
            if(int(time.time())-int(b[i].time)>120):
                b[i].expired='True'
                b[i].save()
        Buffer.objects.filter(expired='True').delete()
        b=Buffer.objects.all()
        for i in b:
            passcodes.append(int(i.passcode))
        passcodes=set(passcodes)
        l=len(passcodes)
        new_passcodes=set()
        lenn=0
        while(lenn!=l+1):
            new_passcodes.add(random.randint(10000,99999))
            lenn=len(new_passcodes)
        new=random.randint(10000,99999)
        for i in new_passcodes:
            if(i not in passcodes):
                new=i
                break
        b=Buffer.objects.create(amount=money,mobile=request.user.username,expired='False',passcode=str(new),time=int(time.time()))
        b.save()


        return render(request,'customer/passcodeDisplay.html',{'passcode':new})
    else:
        return render(request,'customer/money.html')


def transactions(request):
    t=Transactions.objects.all()
    arr=[]
    for i in t:
        if(i.to_User == request.user.username  or i.from_User==request.user.username  ):
            arr.append( [ int(i.time) , i ] )
    arr=sorted(arr)
    arr=arr[::-1]
    for i in range(len(arr)):
        arr[i]=arr[i][1]
    return render(request,'customer/transactions.html',{'arr':arr,'mob':request.user.username})



def receive(request):
    return render(request,'customer/receive.html')

def result(request):
    passcode=request.POST['passcode']
    b=Buffer.objects.all()
    passcodes={}

    for i in range(len(b)):
        if(int(time.time())-int(b[i].time)>120):
            b[i].expired='True'
            b[i].save()
    Buffer.objects.filter(expired='True').delete()

    for i in b:
        passcodes[i.passcode]=[i.mobile,i.amount]
    if(passcode not in passcodes):
        return render(request,'customer/failed.html')
    else:
        mobno,amount=passcodes[passcode]
        if(mobno==request.user.username):
            return render(request,'customer/failed.html')
        Buffer.objects.filter(passcode=passcode).delete()
        t=Transactions.objects.create(from_User=mobno,to_User=request.user.username,time=str(int(time.time())),amount=amount)
        t.save()
        b=Profile.objects.all()
        for i in range(len(b)):
            if(b[i].mobile==mobno):
                b[i].balance-=int(amount)
                b[i].save()
            if(b[i].mobile==request.user.username):
                b[i].balance+=int(amount)
                b[i].save()


        return render(request,'customer/success.html')
    return render(request,'customer/result.html',{'b':b,'pa':passcode})






def profile(request):
    return render(request,'customer/profile.html')






def customer_home(request):
    if(request.user.is_authenticated and request.user.username=='admin'):
        return render(request,'RestrictedAccess.html')
    elif(request.user.is_authenticated and request.user.username!='admin'):
        return render(request,'customer/dashboard.html')

    return render(request,'customer/home.html')


def admin_home(request):
    if(request.user.is_authenticated and request.user.username=='admin'):
        return render(request,'admin/dashboard.html')
    if(request.user.is_authenticated and request.user.username=='admin'):
        return render(request,'RestrictedAccess.html')
    if(request.method=='POST'):
        if(request.POST['mobno']=='admin'):
            print(request.POST['mobno'],request.POST['password'])
            password=request.POST['password']
            user=authenticate(username='admin',password=password)
            if(user is None):
                return render(request,'admin/home.html')
            auth_login(request,user)

            return render(request,'admin/dashboard.html')
        else:
            return render(request,'admin/home.html')
    else:
        return render(request,'admin/home.html')


def admin_dashboard(request):
    if(request.user.is_authenticated and request.user.username!='admin'):
        return render(request,'RestrictedAccess.html')

    if(request.user.is_authenticated and request.user.username=='admin'):
        return render(request,'admin/dashboard.html')

    else:
        return render(request,'admin/home.html')



def customer_dashboard(request):
    if(request.user.is_authenticated and request.user.username=='admin'):
        return render(request,'RestrictedAccess.html')
    if(request.user.is_authenticated and request.user.username!='admin'):
        return render(request,'customer/dashboard.html')
    else:
        return render(request,'customer/login.html')




def login(request):
    if(request.user.is_authenticated):
        return render(request,'customer/dashboard.html')
    if(request.method=='POST'):
        mobno=request.POST['mobno']
        password=request.POST['password']
        q=User.objects.filter(username=mobno)
        if(len(q)==0):
            return render(request,'customer/login.html')
        else:
            user=authenticate(username=mobno,password=password)
            if(user is None):
                return render(request,'customer/login.html')

            auth_login(request,user)
            return render(request,'customer/dashboard.html')

    else:
        return render(request,'customer/login.html')


def register(request):
    if(request.user.is_authenticated):
        return render(request,'customer/dashboard.html')
    if(request.method=='POST'):
        mobno=request.POST['mobno']
        password=request.POST['password']
        email=request.POST['email']
        accountno=request.POST['accountno']
        name=request.POST['name']
        q=User.objects.filter(username=mobno)
        if(len(q)>=1):
            return render(request,'customer/register.html')

        user=User.objects.create_user(password=password,username=mobno)
        p=Profile.objects.create(email=email,name=name,mobile=mobno,accountno=accountno)
        p.save()
        auth_login(request,user)
        return render(request,'customer/dashboard.html')
    else:
        return render(request,'customer/register.html')



def logout(request):
    auth_logout(request)
    return render(request,'customer/login.html')
