from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.contrib.auth.models import User


class CurrentUserSerializer(serializers.ModelSerializer):
    '''Serializer for current User

    Attributes:
    first_name (str)
    last_name (str)
    username (str)
    password (str)
    email (str)
    date_joined (str): date user joined Dram Journal in 'YYYY-MM-DD' format.
    '''
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'password', 'email', 'date_joined']
        # Don't include password in serialized output.
        extra_kwargs = {'password': {'write_only': True}}

# Authenticate requests by token.


@authentication_classes([TokenAuthentication])
# Only allow access for authenticated requests.
@permission_classes([IsAuthenticated])
class CurrentUserView(APIView):
    def get(self, request, *args, **kwargs):
        '''Gets current User's data.

        Parameters:
        request (obj): an instance of Django class HttpRequest, 
        representing the incoming HTTP request.
        *args (tuple): Additional positional arguments passed to the method.
        **kwargs (dict): Additional keyword arguments passed to the method.

        Returns: current User's serialized data.
        '''

        # Create an instance of CurrentUserSerializer with the current user as the instance data.
        serializer = CurrentUserSerializer(request.user)
        # Return a Response with the serialized data of the current user.
        return Response(serializer.data)
