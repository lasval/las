# test_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_app, name="test-app"),
]
