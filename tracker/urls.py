from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path("", views.RegisterTermView.as_view(), name="index"),
    path("register/", views.RegisterTermView.as_view(), name="register_term"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
]
