from django.urls import path
from . import views

urlpatterns = [
    path('sd/', views.sdpage, name='sdpage'),
    path("signup/<int:course_id>/",views.signup_course,name="signup_course"),
    path("search-courses/",views.search_courses,name="search_courses"),
    path('profile/',views.profile,name='profile'),
    path("delete-course/<int:enrollment_id>/",views.delete_course,name="delete_course"),
    path( "edit-profile/", views.edit_profile, name="edit_profile" ), 
    path( 'change-password/', views.change_password, name='change_password' ),
    path('reset-password-email/',views.reset_password_email,name='reset_password_email'),
    path(
    'reset-pass/<int:uid>/<str:token>/',
    views.reset_pass,
    name='reset_pass'
),

    ]
    

