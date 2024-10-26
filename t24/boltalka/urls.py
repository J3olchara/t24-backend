from django.urls import path
from . import views

urlpatterns = [
    path('chat', views.BoltalkaMain.as_view()),
]
