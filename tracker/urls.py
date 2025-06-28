from django.urls import path

from . import views

urlpatterns = [
    path("", views.RegisterTermView.as_view(), name="index"),
    path("register/", views.RegisterTermView.as_view(), name="register_term"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path(
        "delete_livro/<str:livro_name>",
        views.DashboardView.as_view(),
        name="delete_livro",
    ),
    path(
        "delete_term/<int:term_id>/",
        views.DeleteTermView.as_view(),
        name="delete_term",
    ),
]
