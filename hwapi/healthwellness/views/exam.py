from rest_framework.generics import GenericAPIView
from ..models import MedicalExam
from ...utils.controllers import PatientController, AppResponse, DateController
from ..serializers import MedicalExamDoctorSerializer


class MedicalExamView(GenericAPIView):

    @staticmethod
    def get(request):
        try:
            uid = request.uid

            patient_obj = PatientController.get_patient_by_uid(uid)

            exams_obj = MedicalExam.objects.filter(patient=patient_obj.id)
            exams_s = MedicalExamDoctorSerializer(exams_obj, many=True)

            data = exams_s.data

            for exam in data:
                exam['creation_date'] = DateController.format_date_to_local(exam['creation_date'])

            return AppResponse.get_success(data=data)
        except Exception as e:
            return AppResponse.get_error(reason=str(e))