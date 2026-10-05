from django.urls import path
from . import views

urlpatterns = [
    path("", views.landingpage, name="landingpage"),
    path("dashboard.html/", views.dashboard, name="dashboard"),
    path("students/<int:pk>/delete/", views.delete_student, name="delete_student"),
]
