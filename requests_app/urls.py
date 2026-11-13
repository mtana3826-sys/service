from django.urls import path
from . import views

urlpatterns = [
    path("", views.request_list, name="request_list"),
    path("create/", views.request_create, name="request_create"),
    path("<int:pk>/", views.request_detail, name="request_detail"),
    path("<int:pk>/status/", views.update_status, name="update_status"),
]