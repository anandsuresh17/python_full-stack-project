import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.conf import settings
from django.core.mail import EmailMessage
from django.core import signing
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout

from .models import Students, Contact, Profile
from .forms import Studentform, ContactForm


def homepage(request):
    return render(request, "home.html")


def aboutpage(request):
    return render(request, "about.html")


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
                        'error': (
                            'Unable to send an email right now. '
                            'Please try again later.'
                        )
                    }
                )

    else:

        form = ContactForm()

    return render(
        request,
        'contact.html',
        {
            'form': form
                })

def registrationpage(request):

    if request.method == "POST":

        form = Studentform(
            request.POST,
            request.FILES
        )

        print("FORM VALID:", form.is_valid())
        print("FORM ERRORS:", form.errors)

        if form.is_valid():

            try:

                email = form.cleaned_data['email'].strip().lower()

                print("EMAIL:", email)
                print(
                    "EMAIL EXISTS:",
                    User.objects.filter(username=email).exists()
                )

                # Check whether this email is already used
                if User.objects.filter(username=email).exists():

                    return render(
                        request,
                        'registration.html',
                        {
                            'forms': form,
                            'error': (
                                'An account with this email '
                                'already exists.'
                            )
                        }
                    )

                with transaction.atomic():

                    # Generate temporary password
                    temp_password = get_random_string(10)

                    print("TEMP PASSWORD GENERATED")

                    # Create Django User
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=temp_password
                    )

                    print("USER CREATED:", user.username)

                    # Create Student
                    student = form.save(commit=False)

                    student.user = user
                    student.email = email

                    student.country = request.POST.get('country')
                    student.state = request.POST.get('state')
                    student.city = request.POST.get('city')

                    student.first_login = True
                    student.email_verified = False

                    student.save()

                    print("STUDENT CREATED:", student.id)

                    # Create Profile
                    Profile.objects.create(
                        user=user
                    )

                    print("PROFILE CREATED")

                    # Create validation token
                    validation_token = signing.dumps(
                        {
                            'student_id': student.id,
                            'email': student.email
                        }
                    )

                    # Create validation URL
                    verification_url = (
                        "http://127.0.0.1:8000"
                        + reverse(
                            'verify_email',
                            kwargs={
                                'token': validation_token
                            }
                        )
                    )

                    print("VERIFICATION URL CREATED")

                    # Send registration email
                    email_message = EmailMessage(
                        subject='Registration Confirmation',
                        body=(
                            f"Hello {student.fname},\n\n"
                            "Your registration was successful.\n\n"
                            "Please confirm your email by clicking "
                            "the link below:\n\n"
                            f"{verification_url}\n\n"
                            "Your temporary password is:\n"
                            f"{temp_password}\n\n"
                            "You can use this temporary password "
                            "to sign in for the first time.\n\n"
                            "You will be asked to create a new "
                            "password after your first login.\n\n"
                            "Thank you."
                        ),
                        from_email=settings.EMAIL_HOST_USER,
                        to=[student.email]
                    )

                    email_message.send(
                        fail_silently=False
                    )

                    print("EMAIL SENT")

                print("REGISTRATION SUCCESSFUL")

                # Registration successful
                return render(
                    request,
                    'login.html',
                    {
                        'success': (
                            'Registration successful! '
                            'Please check your email for your '
                            'validation link and temporary password.'
                        )
                    }
                )
    
            except Exception as e:

                print(
                    "REGISTRATION ERROR:",
                    repr(e)
                )

                return render(
                    request,
                    'registration.html',
                    {
                        'forms': form,
                        'error': (
                            'Unable to register. '
                            'Please try again.'
                        )
                    }
                )

    else:

        form = Studentform()

    return render(
        request,
        'registration.html',
        {
            'forms': form
        }
    )


def verify_email(request, token):

    try:

        data = signing.loads(
            token,
            max_age=86400
        )

        student_id = data['student_id']
        email = data['email']

        student = Students.objects.get(
            id=student_id,
            email=email
        )

        student.email_verified = True
        student.save(
            update_fields=['email_verified']
        )

        return render(
            request,
            'login.html',
            {
                'success': (
                    'Email verified successfully. '
                    'You can now sign in.'
                )
            }
        )

    except signing.BadSignature:

        return render(
            request,
            'login.html',
            {
                'error': 'Invalid validation link.'
            }
        )

    except signing.SignatureExpired:

        return render(
            request,
            'login.html',
            {
                'error': (
                    'This validation link has expired.'
                )
            }
        )

    except Students.DoesNotExist:

        return render(
            request,
            'login.html',
            {
                'error': (
                    'Unable to verify this email.'
                )
            }
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
        json={
            "country": country
        }
    )

    return JsonResponse(response.json())


def get_cities(request):

    country = request.GET.get("country")
    state = request.GET.get("state")

    url = (
        "https://countriesnow.space/"
        "api/v0.1/countries/state/cities"
    )

    response = requests.post(
        url,
        json={
            "country": country,
            "state": state
        }
    )

    return JsonResponse(response.json())

def loginpage(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        # Keep me logged in checkbox
        keep_logged_in = request.POST.get("keep_logged_in")

        print("LOGIN EMAIL:", email)
        print("KEEP ME LOGGED IN:", keep_logged_in)

        try:

            student = Students.objects.get(
                user__username=email
            )

            print("STUDENT FOUND:", student)
            print("EMAIL VERIFIED:", student.email_verified)
            print("FIRST LOGIN:", student.first_login)

        except Students.DoesNotExist:

            print("STUDENT NOT FOUND")

            return render(
                request,
                "login.html",
                {
                    "error": "Invalid email or password."
                }
            )

        # Check email verification
        if not student.email_verified:

            print("EMAIL NOT VERIFIED")

            return render(
                request,
                "login.html",
                {
                    "error": (
                        "Please verify your email "
                        "before signing in."
                    )
                }
            )

        # Authenticate user
        user = authenticate(
            request,
            username=email,
            password=password
        )

        print("AUTHENTICATE RESULT:", user)

        if user is not None:

            print("LOGIN SUCCESS")

            login(request, user)

            # --------------------------------
            # KEEP ME LOGGED IN
            # --------------------------------

            if keep_logged_in:

                print("KEEP ME LOGGED IN → 14 DAYS")

                request.session.set_expiry(
                    1209600
                )  # 14 days

            else:

                print(
                    "KEEP ME LOGGED IN NOT SELECTED "
                    "→ BROWSER SESSION"
                )

                request.session.set_expiry(0)

            # --------------------------------
            # FIRST LOGIN
            # --------------------------------

            if student.first_login:

                print(
                    "FIRST LOGIN → NEW PASSWORD"
                )

                return redirect("new_password")

            # --------------------------------
            # NORMAL LOGIN
            # --------------------------------

            print(
                "NORMAL LOGIN → DASHBOARD"
            )

            return redirect("sdpage")

        print("INVALID PASSWORD")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid email or password."
            }
        )

    return render(
        request,
        "login.html"
    )

def new_password(request):

    if not request.user.is_authenticated:
        return redirect("login")

    try:

        student = Students.objects.get(
            user=request.user
        )

    except Students.DoesNotExist:

        return redirect("login")

    if not student.first_login:

        return redirect("login")

    if request.method == "POST":

        new_password_value = request.POST.get(
            "new_password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if not new_password_value or not confirm_password:

            return render(
                request,
                "new_password.html",
                {
                    "error": "Please fill in both password fields."
                }
            )

        if new_password_value != confirm_password:

            return render(
                request,
                "new_password.html",
                {
                    "error": "Passwords do not match."
                }
            )

        if len(new_password_value) < 8:

            return render(
                request,
                "new_password.html",
                {
                    "error": (
                        "Password must contain at least "
                        "8 characters."
                    )
                }
            )

        request.user.set_password(
            new_password_value
        )

        request.user.save()

        student.first_login = False

        student.save(
            update_fields=["first_login"]
        )

        update_session_auth_hash(
            request,
            request.user
        )

        return redirect("sdpage")

    return render(
        request,
        "new_password.html"
    )
def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get('email').strip().lower()

        try:

            user = User.objects.get(
                username=email
            )

            student = Students.objects.get(
                user=user
            )

            # Generate new temporary password
            temp_password = get_random_string(10)

            # Set temporary password
            user.set_password(temp_password)
            user.save()

            # Force new password after login
            student.first_login = True
            student.save(update_fields=['first_login'])

            # Send temporary password
            email_message = EmailMessage(
                subject='Password Reset',
                body=(
                    f"Hello {student.fname},\n\n"
                    "Your password has been reset.\n\n"
                    "Your temporary password is:\n"
                    f"{temp_password}\n\n"
                    "Please use this password to sign in.\n\n"
                    "After signing in, you will be asked "
                    "to create a new password.\n\n"
                    "Thank you."
                ),
                from_email=settings.EMAIL_HOST_USER,
                to=[student.email]
            )

            email_message.send(
                fail_silently=False
            )

            return render(
                request,
                'forgot_password.html',
                {
                    'success': (
                        'A temporary password has been '
                        'sent to your email.'
                    )
                }
            )

        except Exception as e:

            print("FORGOT PASSWORD ERROR:", e)

            return render(
                request,
                'forgot_password.html',
                {
                    'error': (
                        'Unable to reset password. '
                        'Please check your email and try again.'
                    )
                }
            )

    return render(
        request,
        'forgot_password.html'
    )
def logoutpage(request):

    logout(request)

    return redirect("login")


