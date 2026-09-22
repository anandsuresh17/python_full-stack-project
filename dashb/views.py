from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.urls import reverse
from django.core.mail import send_mail



from apps1.models import (
    CoursesList,
    Profile,
    CourseEnrollment,Students
)
from apps1.forms import Studentform


@login_required
def sdpage(request):

    courses = CoursesList.objects.all()

    profile = Profile.objects.get(
        user=request.user
    )

    enrollments = CourseEnrollment.objects.filter(
        profile=profile
    )

    return render(
        request,
        "sd.html",
        {
            "courses": courses,
            "enrollments": enrollments
        }
    )


@login_required
def signup_course(request, course_id):

    profile = Profile.objects.get(
        user=request.user
    )

    course = CoursesList.objects.get(
        id=course_id
    )

    CourseEnrollment.objects.create(
        profile=profile,
        course=course
    )

    return redirect("sdpage")


@login_required
def search_courses(request):

    search = request.GET.get("search", "")

    courses = CoursesList.objects.filter(
        course_name__icontains=search
    )

    data = []

    for course in courses:
        data.append({
            "id": course.id,
            "course_name": course.course_name,
            "duration": course.duration,
            "fee": str(course.fee)
        })

    return JsonResponse({
        "courses": data
    })
@login_required
def profile(request):

    student = Students.objects.get(
        user=request.user
    )

    return render(
        request,
        "profile.html",
        {
            "student": student
        }
    )

@login_required
def delete_course(request, enrollment_id):

    enrollment = CourseEnrollment.objects.get(
        id=enrollment_id,
        profile__user=request.user
    )

    enrollment.delete()

    return redirect("sdpage")

@login_required
def edit_profile(request):

    student = Students.objects.get(
        user=request.user
    )

    if request.method == "POST":

        form = Studentform(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():

            student = form.save(
                commit=False
            )

            # Country, state and city
            # are handled manually
            student.country = request.POST.get("country")
            student.state = request.POST.get("state")
            student.city = request.POST.get("city")

            student.save()

            # Update Django User when email is changed
            request.user.username = student.email
            request.user.email = student.email
            request.user.save()

            return redirect("profile")

    else:

        form = Studentform(
            instance=student
        )

    return render(
        request,
        "edit_profile.html",
        {
            "form": form,
            "student": student
        }
    )

@login_required
def change_password(request):

    if request.method == "POST":

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(old_password):

            return render(
                request,
                "change_password.html",
                {
                    "error": "Existing password is incorrect."
                }
            )

        if new_password != confirm_password:

            return render(
                request,
                "change_password.html",
                {
                    "error": "New passwords do not match."
                }
            )

        request.user.set_password(new_password)
        request.user.save()

        # Use existing logout functionality
        return redirect("logout")

    return render(
        request,
        "change_password.html"
    )



@login_required
def reset_password_email(request):

    user = request.user

    token = default_token_generator.make_token(user)

    reset_url = request.build_absolute_uri(
        reverse(
            "reset_pass",
            kwargs={
                "uid": user.id,
                "token": token
            }
        )
    )

    send_mail(
        "Reset Your Password",
        f"""
Click the link below to reset your password:

{reset_url}

If you did not request this, you can ignore this email.
""",
        None,
        [user.email],
    )

    return render(
        request,
        "change_password.html",
        {
            "message": "Password reset link has been sent to your email."
        }
    )


def reset_pass(request, uid, token):

    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return render(
            request,
            "newpass.html",
            {"error": "Invalid password reset link."}
        )

    if not default_token_generator.check_token(user, token):
        return render(
            request,
            "newpass.html",
            {"error": "Password reset link is invalid or expired."}
        )

    if request.method == "POST":

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(
                request,
                "newpass.html",
                {"error": "Passwords do not match."}
            )

        user.set_password(password)
        user.save()

        return redirect("logout")

    return render(request, "newpass.html")