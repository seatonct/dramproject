from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from dramapi.models import Entry, Bookmark
from .entries import EntrySerializer


class BookmarkSerializer(serializers.ModelSerializer):
    '''Serializer for Bookmark model

    Attribute:
        id (int): primary key for the Bookmark
        entry (int): primary key of related Entry
        user (int): primary key of related User, the owner of the Bookmark
        is_owner (bool): indicates whether current user is owner of the Bookmark
        '''
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ['id', 'entry', 'user', 'is_owner']
        read_only_fields = ['user']

    def get_is_owner(self, obj):
        '''Checks whether the current user is the owner of the Bookmark

        Parameters:
        obj (obj): an instance of the class Bookmark

        Returns: Boolean

        '''

        return self.context['request'].user == obj.user


class MyBookmarksSerializer(serializers.ModelSerializer):
    '''Serializer for Bookmark model that includes 'entry' field.

    Attribute:
        id (int): primary key for the Bookmark
        entry (dict): all data included in the related Entry
        user (int): primary key of related User, the owner of the Bookmark
        is_owner (bool): indicates whether current user is owner of the Bookmark
        '''

    entry = EntrySerializer(many=False)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ['id', 'entry', 'user', 'is_owner']
        read_only_fields = ['user']

    def get_is_owner(self, obj):
        '''Checks whether the current user is the owner of the Bookmark

        Parameters:
        obj (obj): an instance of the class Bookmark

        Returns: Boolean

        '''
        return self.context['request'].user == obj.user


class BookmarkViewSet(viewsets.ViewSet):
    # Allow any user to access, regardless of authentication.
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        '''Lists Bookmark instances, 
        filtered according to query_params (if present), 
        in descending order by 'id'

        Parameters:
        request (obj): an instance of Django class HttpRequest, 
        representing the incoming HTTP request.

        Returns: List of Bookmark dictionaries with 200 status code'''

        # If 'username' is included in 'query_params', assign its value to a variable.
        username = request.query_params.get('username')

        # If 'expand' is included in 'query_params', assign its value to a variable.
        expansion = request.query_params.get('expand')

        # Get all bookmarks, in descending order by 'id'
        bookmarks = Bookmark.objects.all().order_by('-id')

        # If 'username' was included in 'query_params', filter bookmarks by username.
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            bookmarks = bookmarks.filter(
                user=user)

        # If 'expand' was included in 'query_params', expand the designated field.
        if expansion == 'entry':
            # Serialize the objects, and pass request to determine owner.
            serializer = MyBookmarksSerializer(
                bookmarks, many=True, context={'request': request})
        else:
            # Serialize the objects, and pass request to determine owner.
            serializer = BookmarkSerializer(
                bookmarks, many=True, context={'request': request})

        # Return the serialized data with 200 status code
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        '''Creates a new instance of class Bookmark.

        Parameters:
        request (obj): an instance of Django class HttpRequest, 
        representing the incoming HTTP request.

        Returns: newly created Bookmark instance with 201 status code; 
        otherwise, Exception with 400 status code.'''

        # Assign pk of Entry being bookmarked to a variable.
        bookmarked_entry = Entry.objects.get(pk=request.data['entryId'])

        # Create a new instance of a Bookmark and assign property
        # values from the request payload using `request.data`
        bookmark = Bookmark()
        bookmark.user = request.user
        bookmark.entry = bookmarked_entry
        bookmark.save()

        try:
            # Serialize the objects, and pass request as context
            serialized = BookmarkSerializer(
                bookmark, many=False, context={'request': request})
            # Return the serialized data with 201 status code
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        except Exception:
            # If creation of Bookmark fails, return 400 status code.
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        '''Get a single Bookmark.

        Parameters:
        request (obj): an instance of Django class HttpRequest, 
        representing the incoming HTTP request.
        pk (int): primary key of the bookmark to be retrieved.

        Returns: the requested Bookmark instance with 200 status code;
        otherwise, Exception with 404 status code.
        '''

        try:
            # Get the requested Bookmark
            bookmark = Bookmark.objects.get(pk=pk)
            # Serialize the object, and pass request as context.
            serializer = BookmarkSerializer(
                bookmark, context={'request': request})
            # Return the Bookmark with 200 status code
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Bookmark.DoesNotExist:
            # If Bookmark doesn't exist, return 404 status code.
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        '''Delete a Bookmark instance.

        Parameters:
        request (obj): an instance of Django class HttpRequest, 
        representing the incoming HTTP request.
        pk (int): primary key of the bookmark to be deleted.

        Returns:
        204 status code if successful.
        403 if User is not owner of Bookmark.
        404 if Bookmark does not exist.
        '''

        try:
            # Get the requested Bookmark
            bookmark = Bookmark.objects.get(pk=pk)

            # Check if the User has permission to delete
            # Will return 403 if authenticated User is not owner
            if bookmark.user.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Delete the Bookmark
            bookmark.delete()

            # Return success but no body
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Bookmark.DoesNotExist:
            # Return 404 status code.
            return Response(status=status.HTTP_404_NOT_FOUND)
