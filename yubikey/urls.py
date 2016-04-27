from django.conf.urls import url
from django.contrib import admin

from yubikey import views

urlpatterns = [
    url(r'^yubikey-auth', views.AuthView.as_view(), name='yubikey-auth'),
]