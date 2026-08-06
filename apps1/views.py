
from django.shortcuts import render,redirect
from.models import Students
from .forms import Studentform
def homepage(request):
    return render(request, "home.html")

def aboutpage(request):
    return render(request, "about.html")

def contactpage(request):
    return render(request, "contact.html")

def registrationpage(request):
    if request.method=="POST":
        form=Studentform(request.POST,request.FILES)
        if form.is_valid():
            form.save()

            # return redirect('emp')

    else:
        form= Studentform()
    return render(request,'registration.html',{'forms':form})

def loginpage(request):
    return render(request, "login.html")

def sdpage(request):
    return render(request, "sd.html")
