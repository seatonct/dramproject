from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from dramapi.models import Color


class ColorSerializer(serializers.ModelSerializer):
    '''Serializer for Color model

    Attributes:
        id (int): primary key for the Color
        label (str): name/description of the Color
        color_grade (float): rating in range 0.0-2.0
        hex_code (str): hex code of Color
        tailwind_name (str): custom Tailwind color name'''

    class Meta:
        model = Color
        fields = ['id', 'label', 'color_grade', 'hex_code', 'tailwind_name']


class ColorViewSet(viewsets.ViewSet):

    def list(self, request):
        '''Lists Color instances.

        Parameters:
        request (obj): an instance of Django class HttpRequest, 
        representing the incoming HTTP request.

        Returns: List of Bookmark dictionaries with 200 status code'''

        # Get all colors.
        colors = Color.objects.all()
        # Serialize the objects.
        serializer = ColorSerializer(colors, many=True)
        # Return the serialized data with 200 status code.
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''Get a single Color.

        Parameters:
        request (obj): an instance of Django class HttpRequest, 
        representing the incoming HTTP request.
        pk (int): primary key of the Color to be retrieved.

        Returns: the requested Color instance with 200 status code;
        otherwise, Exception with 404 status code.'''

        try:
            # Get the requested Color.
            color = Color.objects.get(pk=pk)
            # Serialize the object.
            serializer = ColorSerializer(color)
            # Return the Color with a 200 status code.
            return Response(serializer.data)
        except Color.DoesNotExist:
            # If the Color doesn't exist, return 404 status code.
            return Response(status=status.HTTP_404_NOT_FOUND)
