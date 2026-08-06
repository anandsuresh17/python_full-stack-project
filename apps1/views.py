from django.shortcuts import render

def homepage(request):
    return render(request, "home.html")

def aboutpage(request):
    return render(request, "about.html")

def contactpage(request):
    return render(request, "contact.html")

def registrationpage(request):
    return render(request, "registration.html")

def loginpage(request):
    return render(request, "login.html")

def sdpage(request):
    return render(request, "sd.html")
