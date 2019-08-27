from django.shortcuts import render
from .models import Profile
# Create your views here.



def home(request):
    list=Profile.objects.all()
    return render(request,'home.html',{'list':list})

def post(request):
    if(request.method=='POST'):

        name=request.POST['name']
        p=Profile.objects.create(name=name)
        p.save()
        list=Profile.objects.all()
        return render(request,'home.html',{'list':list})

    else:
        return render(request,'post.html')
