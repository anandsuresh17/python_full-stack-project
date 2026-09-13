from django.contrib import admin
from .models import Students, CoursesList, Profile, CourseEnrollment, Contact


admin.site.register(Students)
admin.site.register(CoursesList)
admin.site.register(Profile)
admin.site.register(CourseEnrollment)
admin.site.register(Contact)