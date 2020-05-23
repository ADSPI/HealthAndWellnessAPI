from django.urls import path
from .views import *

urlpatterns = [
    path('authenticate', AuthView.as_view()),
]
