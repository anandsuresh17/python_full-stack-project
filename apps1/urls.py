from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('about/', views.aboutpage, name='about'),
    path('contact/', views.contactpage, name='contact'),
    path('registration/', views.registrationpage, name='registration'),
    path('login/', views.loginpage, name='login'),
    path('verify-email/<str:token>/',views.verify_email,name='verify_email'),
    path('new-password/',views.new_password,name='new_password'),
    path('forgot-password/',views.forgot_password,name='forgot_password'),
    path('logout/',views.logoutpage,name='logout'),
    path('python/', views.python_course, name='python_course'),
    path('java/', views.java_course, name='java_course'),
    path('mern/', views.mern_course, name='mern_course'),
    path('react/', views.react_course, name='react_course'),
    path('testing/', views.testing_course, name='testing_course'),
    path('uiux/', views.uiux_course, name='uiux_course'),
    path('data-analytics/', views.data_analytics_course, name='data_analytics_course'),


    ]
