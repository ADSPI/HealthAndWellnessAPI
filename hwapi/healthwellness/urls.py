from django.urls import path
from .views import *

urlpatterns = [
    path('patient-auth', PatientAuthView.as_view()),
    path('patient', PatientView.as_view()),
    path('patient-token', PatientTemporaryToken.as_view())
]
