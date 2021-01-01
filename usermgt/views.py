from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, ]


class UnprotectedView(APIView):
    def get(self, request):
        response = {'message': 'Unprotected view'}
        return Response(response)


class ProtectedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        response = {'message': 'Protected view'}
        return Response(response)
