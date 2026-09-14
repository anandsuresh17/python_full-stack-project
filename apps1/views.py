
import requests

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMessage


from .models import Students,Contact
from .forms import Studentform,ContactForm
def homepage(request):
    return render(request, "home.html")

def aboutpage(request):
    return render(request, "about.html")

def contactpage(request):
    return render(request, "contact.html")
from django.shortcuts import render
from .forms import Studentform


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

    return render(
        request,
        'registration.html',
        {'forms': form}
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

def contactpage(request):

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():

            contact_data = form.save()

            try:

                email = EmailMessage(
                    subject=contact_data.subject,
                    body=(
                        f"Name: {contact_data.name}\n"
                        f"Email: {contact_data.email}\n\n"
                        f"Message:\n{contact_data.message}"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    to=['eduhubarg72@gmail.com'],
                    reply_to=[contact_data.email],
                )

                email.send(fail_silently=False)

                return render(
                    request,
                    'contact.html',
                    {
                        'form': ContactForm(),
                        'success': 'Your message has been sent successfully.'
                    }
                )

            except Exception as e:

                print("EMAIL ERROR:", e)

                return render(
                    request,
                    'contact.html',
                    {
                        'form': form,
                        'error': 'Unable to send an email right now. Please try again later.'
                    }
                )

    else:

        form = ContactForm()

    return render(
        request,
        'contact.html',
        {
            'form': form
        }
    )