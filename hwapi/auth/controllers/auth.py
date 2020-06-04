from ...healthwellness.models import Patient


class AuthController:

    @staticmethod
    def get_patient_by_email(email):
        try:
            patient: Patient = Patient.objects.filter(email=email).first()
            return patient
        except Exception as e:
            raise e
