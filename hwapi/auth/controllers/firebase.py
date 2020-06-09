from firebase_admin import auth
import requests
import json
from ..exceptions import ForbiddenException

FIREBASE_KEY = 'AIzaSyCX0iLmpJ6MSc5WTdqfGtSdWLX3MPth5S4'
FIREBASE_ENDPOINT = 'https://identitytoolkit.googleapis.com/v1/'


class FirebaseController:

    @staticmethod
    def create_firebase_user(email, password):
        try:
            firebase_user = auth.create_user(email=email, password=password)
            return firebase_user
        except Exception as error:
            raise error

    @staticmethod
    def get_uid_from_token(token):
        try:
            res = auth.verify_id_token(token, check_revoked=True)
            return res['uid']
        except Exception as e:
            raise e

    @staticmethod
    def validate_request(request):
        try:
            token = request.META['HTTP_ACCESSTOKEN']
            return FirebaseController.get_uid_from_token(token)
        except Exception:
            raise ForbiddenException

    @staticmethod
    def refresh_id_token(refresh_token):
        try:
            endpoint = 'https://securetoken.googleapis.com/v1/token?key=' + FIREBASE_KEY
            headers = {'Content-type': 'x-www-form-urlencoded'}
            payload = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }

            response = requests.post(endpoint, data=json.dumps(payload), headers=headers)
            response = json.loads(response.content)

            return response

        except Exception as error:
            raise error

    @staticmethod
    def reset_password(email, language='en'):
        try:
            endpoint = 'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=' + FIREBASE_KEY
            headers = {'X-Firebase-Locale': language}
            payload = {
                'requestType': 'PASSWORD_RESET',
                'email': email
            }

            response = requests.post(endpoint, data=json.dumps(payload), headers=headers)
            response = json.loads(response.content)

            return response

        except Exception as error:
            raise error

    @staticmethod
    def get_user_by_email_and_password(email, password):
        try:
            result = {
                'success': False,
                'data': None,
                'message': ''
            }

            endpoint = FIREBASE_ENDPOINT+'accounts:signInWithPassword?key='+FIREBASE_KEY
            headers = {'Content-type': 'application/json'}
            payload = {
                'email': email,
                'password': password,
                'returnSecureToken': True
            }

            response = requests.post(endpoint, data=json.dumps(payload), headers=headers)
            response = json.loads(response.content)

            error = response.get('error', None)

            if error is not None:
                result['message'] = error['message']
            else:
                result['success'] = True
                result['data'] = response

        except Exception as error:
            raise error
        finally:
            return result

    @staticmethod
    def delete_user(uid):
        try:
            auth.delete_user(uid)
        except Exception as error:
            raise error
