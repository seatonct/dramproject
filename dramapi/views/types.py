from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from dramapi.models import Type


class TypeSerializer(serializers.ModelSerializer):
    '''Serializer for Rating model.

    Attributes:
    id (int)
    label (str): indicates whiskey type, e.g., single malt'''

    class Meta:
        model = Type
        fields = ['id', 'label']


class TypeViewSet(viewsets.ViewSet):

    def list(self, request):
        '''Lists all whiskey Types.

        Parameters:
        request (obj): an instance of Django class HttpRequest, 
        representing the incoming HTTP request.

        Returns: serialized List of whiskey Types.
        '''

        # Get all whiskey Types.
        types = Type.objects.all()
        # Serialize the objects.
        serializer = TypeSerializer(types, many=True)
        # Return serialized data with 200 status code.
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''Get a single whiskey Type.

        Parameters:
        request (obj): an instance of Django class HttpRequest, 
        representing the incoming HTTP request.
        pk (int): primary key of the whiskey Type to be retrieved.

        Returns: the requested whiskey Type instance with 200 status code;
        otherwise, Exception with 404 status code.'''

        try:
            # Get the requested whiskey Type.
            whiskey_type = Type.objects.get(pk=pk)
            # Serialize the object.
            serializer = TypeSerializer(whiskey_type)
            # Return the serialized data with a 200 status code.
            return Response(serializer.data)
        except Type.DoesNotExist:
            # If type doesn't exist, return 404 status code.
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        '''Creates a new instance of class Type.

        Parameters:
        request (obj): an instance of Django class HttpRequest, 
        representing the incoming HTTP request.

        Returns: newly created whiskey Type instance with 201 status code; 
        otherwise, Exception with 400 status code.'''

        label = request.data.get('label')

        post = Type.objects.create(label=label)

        serializer = TypeSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            whiskey_type = Type.objects.get(pk=pk)

            self.check_object_permissions(request, whiskey_type)

            whiskey_type.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Type.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
