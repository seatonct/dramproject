from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from dramapi.models import Entry, Bookmark
from django.contrib.auth.models import User
from .entries import EntrySerializer


class BookmarkSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ['id', 'entry', 'user', 'is_owner']
        read_only_fields = ['user']

    def get_is_owner(self, obj):
        # Check if the user is the owner of the review
        return self.context['request'].user == obj.user


class MyBookmarksSerializer(serializers.ModelSerializer):
    entry = EntrySerializer(many=False)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ['id', 'entry', 'user', 'is_owner']
        read_only_fields = ['user']

    def get_is_owner(self, obj):
        return self.context['request'].user == obj.user


class BookmarkViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        username = request.query_params.get('username')
        expansion = request.query_params.get('expand')
        # Get all bookmarks
        bookmarks = Bookmark.objects.all().order_by('-id')

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            bookmarks = bookmarks.filter(
                user=user)

        if expansion == 'entry':
            serializer = MyBookmarksSerializer(
                bookmarks, many=True, context={'request': request})
        else:
            # Serialize the objects, and pass request to determine owner
            serializer = BookmarkSerializer(
                bookmarks, many=True, context={'request': request})

        # Return the serialized data with 200 status code
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        bookmarked_entry = Entry.objects.get(pk=request.data['entryId'])
        # Create a new instance of a bookmark and assign property
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
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            # Get the requested review
            bookmark = Bookmark.objects.get(pk=pk)
            # Serialize the object (make sure to pass the request as context)
            serializer = BookmarkSerializer(
                bookmark, context={'request': request})
            # Return the review with 200 status code
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Bookmark.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            # Get the requested bookmark
            bookmark = Bookmark.objects.get(pk=pk)

            # Check if the user has permission to delete
            # Will return 403 if authenticated user is not author
            if bookmark.user.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Delete the bookmark
            bookmark.delete()

            # Return success but no body
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Bookmark.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
