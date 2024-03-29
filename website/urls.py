from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from website import views
from .models import *

from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView




urlpatterns = [
    path('', views.HomePage, name='home'),
    path('signup', views.SignupPage, name='signup'),
    path('activate/<uidb64>/<token>', views.ActivatePage, name='activate'),
    path('signin', views.SigninPage, name='signin'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('signout', views.SignoutPage, name='signout'),
    path('contact', views.ContactPage, name='contact'),
    path('about', views.AboutPage, name='about'),
    path('course', views.CoursePage, name='course'),
    path('civil_main', views.Civil_Main_Page, name='civil_main'),
    path('electronic_main', views.Electronic_Main_Page, name='electronic_main'),
    path('info_technology_main', views.Info_Technology_Main_Page, name='info_technology_main'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
