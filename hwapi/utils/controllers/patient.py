from ...healthwellness.models import Patient


class PatientController:

    @staticmethod
    def get_patient_by_uid(uid: str):
        try:
            return Patient.objects.filter(uid=uid).first()
        except Exception as e:
            raise e
