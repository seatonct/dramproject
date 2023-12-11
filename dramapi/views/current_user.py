from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.contrib.auth.models import User


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'password', 'email', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CurrentUserView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)
