from ..auth.controllers.firebase import FirebaseController
from ..auth.exceptions import *
from ..utils.controllers import AppResponse


class AccessMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

        self.not_protected_routes = [
            '/auth/authenticate',
            '/auth/resetpassword',
            '/auth/renew',
            '/hw/patient-auth'
        ]

    def __call__(self, request):

        response = self.get_response(request)

        if response.status_code == 200:

            path = request.path

            if path not in self.not_protected_routes:
                refresh_token = request.META.get('HTTP_REFRESHTOKEN', None)
                renewed_tokens = FirebaseController.refresh_id_token(refresh_token)

                response['refresh-token'] = renewed_tokens['refresh_token']
                response['access-token'] = renewed_tokens['id_token']

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            path = request.path

            if path not in self.not_protected_routes:
                uid = FirebaseController.validate_request(request)

                request.uid = uid
        except ForbiddenException:
            return AppResponse.get_forbidden()
        except UnauthorizedException:
            return AppResponse.get_unauthorized()
        except Exception as e:
            return AppResponse.get_error(reason=str(e))

    def process_exception(self, request, exception):
        if isinstance(exception, UnauthorizedException):
            return AppResponse.get_unauthorized()
        if isinstance(exception, ForbiddenException):
            return AppResponse.get_forbidden()
        return AppResponse.get_error(reason=str(exception))
