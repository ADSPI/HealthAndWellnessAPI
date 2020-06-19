from django.urls import path
from .views import *

urlpatterns = [
    path('patient-auth', PatientAuthView.as_view()),
    path('patient', PatientView.as_view()),
    path('patient-token', PatientTemporaryToken.as_view()),
    path('patient/<int:id_patient>', PatientDetailView.as_view()),

    path('exam', MedicalExamView.as_view()),
    path('exam/<int:id_exam>', MedicalExamDetailView.as_view())
]
