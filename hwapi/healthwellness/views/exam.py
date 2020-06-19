from rest_framework.generics import GenericAPIView
from ..models import MedicalExam
from ...utils.controllers import PatientController, AppResponse, DateController
from ..serializers import MedicalExamDoctorSerializer, MedicalExamSerializer


class MedicalExamView(GenericAPIView):

    @staticmethod
    def get(request):
        try:
            uid = request.uid

            patient_obj = PatientController.get_patient_by_uid(uid)

            exams_obj = MedicalExam.objects.select_related('doctor').filter(patient=patient_obj.id)
            exams_s = MedicalExamDoctorSerializer(exams_obj, many=True)

            data = exams_s.data

            for exam in data:
                exam['creation_date'] = DateController.format_date_to_local(exam['creation_date'])

            return AppResponse.get_success(data=data)
        except Exception as e:
            return AppResponse.get_error(reason=str(e))

    @staticmethod
    def post(request):
        try:
            body = request.data
            uid = request.uid

            id_patient = PatientController.get_patient_id_by_uid(uid)
            body['patient'] = id_patient
            body['creation_date'] = DateController.format_date_to_iso(body['creation_date'])

            exam_s = MedicalExamSerializer(data=body, many=False)
            exam_s.is_valid(raise_exception=True)
            exam_s.save()

            result = exam_s.data
            result['creation_date'] = DateController.format_date_to_local(result['creation_date'])

            return AppResponse.get_success(data=result)

        except Exception as e:
            return AppResponse.get_error(reason=str(e))


class MedicalExamDetailView(GenericAPIView):

    @staticmethod
    def get(request, id_exam):
        try:
            uid = request.uid
            id_patient = PatientController.get_patient_id_by_uid(uid)

            exam_obj = MedicalExam.objects.select_related('patient').get(pk=id_exam)
            if exam_obj.patient.id != id_patient:
                return AppResponse.get_unauthorized()

            exam_s = MedicalExamDoctorSerializer(exam_obj, many=False)
            result = exam_s.data
            result['creation_date'] = DateController.format_date_to_local(result['creation_date'])

            return AppResponse.get_success(data=result)
        except Exception as e:
            return AppResponse.get_error(reason=str(e))

    @staticmethod
    def put(request, id_exam):
        try:
            body = request.data
            uid = request.uid
            id_patient = PatientController.get_patient_id_by_uid(uid)

            exam_obj = MedicalExam.objects.select_related('patient').get(pk=id_exam)
            if exam_obj.patient.id != id_patient:
                return AppResponse.get_unauthorized()

            exam_s = MedicalExamSerializer(exam_obj, data=body, many=False)
            exam_s.is_valid(raise_exception=True)
            exam_s.save()

            result = exam_s.data
            result['creation_date'] = DateController.format_date_to_local(result['creation_date'])

            return AppResponse.get_success(data=result)
        except Exception as e:
            return AppResponse.get_error(reason=str(e))
