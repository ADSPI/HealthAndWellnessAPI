from rest_framework.generics import GenericAPIView
from ...utils.controllers import AppResponse
from ..controllers import AuthController, FirebaseController


class AuthView(GenericAPIView):

    @staticmethod
    def post(request):
        try:
            body = request.data
            result = {}

            email = body['email']
            password = body['senha']

            patient = AuthController.get_patient_by_email(email)

            if patient is not None:
                firebase_data = FirebaseController.get_user_by_email_and_password(email, password)
                result['success'] = firebase_data['success']
                result['data'] = {}
                result['data']['accessToken'] = firebase_data['data']['idToken']
                result['data']['refreshToken'] = firebase_data['data']['refreshToken']
                result['message'] = 'Success'
            else:
                result['success'] = False
                result['data'] = None
                result['message'] = 'Invalid Credentials'

            return AppResponse.auth_response(result)

        except Exception as e:
            return AppResponse.get_error(reason=str(e))
