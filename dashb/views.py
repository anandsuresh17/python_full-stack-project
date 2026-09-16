from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from apps1.models import (
    CoursesList,
    Profile,
    CourseEnrollment
)


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