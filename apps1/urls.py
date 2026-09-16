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
    ]
