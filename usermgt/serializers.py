from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        lookup_field = 'username'
        fields = ['username', 'first_name', 'last_name', 'email',
                  'role', 'department', 'extension', 'position']
