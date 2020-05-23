from rest_framework.generics import GenericAPIView
from ...utils.controllers import AppResponse


class AuthView(GenericAPIView):

    @staticmethod
    def post(request):
        return AppResponse.get_success(data='SUCESS')
