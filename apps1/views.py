
import requests

from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import Students
from .forms import Studentform
def homepage(request):
    return render(request, "home.html")

def aboutpage(request):
    return render(request, "about.html")

def contactpage(request):
    return render(request, "contact.html")
def registrationpage(request):

    if request.method == "POST":

        form = Studentform(request.POST, request.FILES)

        if form.is_valid():

            obj = form.save(commit=False)

            obj.country = request.POST.get('country')
            obj.state = request.POST.get('state')
            obj.city = request.POST.get('city')

            obj.save()

    else:

        form = Studentform()

    return render( request, 'registration.html', {'forms': form}
    )
def get_countries(request):

    url = "https://countriesnow.space/api/v0.1/countries"

    response = requests.get(url)

    return JsonResponse(response.json())


def get_states(request):

    country = request.GET.get("country")

    url = "https://countriesnow.space/api/v0.1/countries/states"

    response = requests.post(
        url,
        json={"country": country}
    )

    return JsonResponse(response.json())


def get_cities(request):

    country = request.GET.get("country")
    state = request.GET.get("state")

    url = "https://countriesnow.space/api/v0.1/countries/state/cities"

    response = requests.post(
        url,
        json={
            "country": country,
            "state": state
        }
    )

    return JsonResponse(response.json())

def loginpage(request):
    return render(request, "login.html")

def sdpage(request):
    return render(request, "sd.html")
