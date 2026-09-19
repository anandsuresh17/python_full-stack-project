from django.urls import path
from . import views

urlpatterns = [
    path('sd/', views.sdpage, name='sdpage'),
    path("signup/<int:course_id>/",views.signup_course,name="signup_course"),
    path("search-courses/",views.search_courses,name="search_courses"
),
    
    ]
