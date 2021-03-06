from rest_framework.generics import GenericAPIView
from ...utils.controllers import AppResponse, PatientController, DateController
from ...auth.controllers.firebase import FirebaseController
from ..serializers import PatientSerializer
from ..models import Patient


class PatientAuthView(GenericAPIView):

    @staticmethod
    def post(request):
        try:
            firebase_user_created = False
            body = request.data

            firebase_user = FirebaseController.create_firebase_user(body['email'], body['password'])
            firebase_user_created = True
            uid = firebase_user.uid

            body['birth_date'] = DateController.format_date_to_iso(body['birth_date'])
            body['uid'] = uid

            new_patient = PatientSerializer(data=body, many=False)
            new_patient.is_valid(raise_exception=True)
            new_patient.save()

            result_data = new_patient.data
            result_data['birth_date'] = DateController.format_date_to_local(result_data['birth_date'])

            return AppResponse.get_success(data=result_data)

        except Exception as e:
            if firebase_user_created:
                FirebaseController.delete_user(uid)
            return AppResponse.get_error(reason=str(e))


class PatientView(GenericAPIView):

    @staticmethod
    def get(request):
        try:
            uid = request.uid

            patient_obj = PatientController.get_patient_by_uid(uid)
            patient_s = PatientSerializer(patient_obj, many=False)

            result = patient_s.data
            result['birth_date'] = DateController.format_date_to_local(result['birth_date'])

            return AppResponse.get_success(data=result)
        except Exception as e:
            return AppResponse.get_error(reason=str(e))


class PatientTemporaryToken(GenericAPIView):

    @staticmethod
    def get(request):
        try:
            uid = request.uid

            custom_token = FirebaseController.create_custom_token(uid)

            result = {
                'custom_token': custom_token.decode('utf-8')
            }

            return AppResponse.get_success(data=result)
        except Exception as e:
            return AppResponse.get_error(str(e))


class PatientDetailView(GenericAPIView):

    @staticmethod
    def put(request, id_patient):
        try:
            uid = request.uid
            body = request.data

            patient_obj = PatientController.get_patient_by_uid(uid)
            if patient_obj.id != id_patient:
                return AppResponse.get_unauthorized()

            body['uid'] = uid
            body['email'] = patient_obj.email
            body['birth_date'] = DateController.format_date_to_iso(body['birth_date'])
            body['id'] = id_patient

            patient_s = PatientSerializer(patient_obj, data=body, many=False)
            patient_s.is_valid(raise_exception=True)
            patient_s.save()

            result = patient_s.data
            result['birth_date'] = DateController.format_date_to_local(result['birth_date'])

            return AppResponse.get_success(data=result)

        except Exception as e:
            return AppResponse.get_error(reason=str(e))
