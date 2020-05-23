from django.http import JsonResponse
from rest_framework import status


class AppResponse:

    @staticmethod
    def get_success(data=None, message=""):
        return JsonResponse({
            'success': True,
            'data': data,
            'message': message
        })

    @staticmethod
    def get_error(reason="Error", statuscode=status.HTTP_500_INTERNAL_SERVER_ERROR):
        return JsonResponse({
            'success': False,
            'reason': reason
        })

    @staticmethod
    def get_forbidden():
        return AppResponse.get_error(reason="Forbidden", status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def get_unauthorized():
        return AppResponse.get_error(reason="Unauthorized", status=status.HTTP_401_UNAUTHORIZED)