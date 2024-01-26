from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from dramapi.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    '''Serializer for Rating model.

    Attributes:
    id (int)
    number_rating (int): rating from 0 to 5
    label (str): description of rating, e.g., 'good'
    '''
    class Meta:
        model = Rating
        fields = ['id', 'number_rating', 'label']


class RatingViewSet(viewsets.ViewSet):

    def list(self, request):
        '''Lists all ratings.

        Parameters:
        request (obj): an instance of Django class HttpRequest, 
        representing the incoming HTTP request.

        Returns: serialized List of ratings.
        '''

        # Get all Ratings.
        ratings = Rating.objects.all()
        # Serialize the objects.
        serializer = RatingSerializer(ratings, many=True)
        # Return the serialized data with 200 status code.
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''Get a single Rating.

        Parameters:
        request (obj): an instance of Django class HttpRequest, 
        representing the incoming HTTP request.
        pk (int): primary key of the Rating to be retrieved.

        Returns: the requested Rating instance with 200 status code;
        otherwise, Exception with 404 status code.'''

        try:
            # Get the requested Rating.
            rating = Rating.objects.get(pk=pk)
            # Serialize the object.
            serializer = RatingSerializer(rating)
            # Return the serialized data with a 200 status code.
            return Response(serializer.data)
        except Rating.DoesNotExist:
            # If the Rating doesn't exist, return 404 status code.
            return Response(status=status.HTTP_404_NOT_FOUND)
