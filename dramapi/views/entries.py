from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from dramapi.models import Entry, Type, Color, Rating
from .types import TypeSerializer
from .colors import ColorSerializer
from .ratings import RatingSerializer


class EntryAuthorSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = User
        fields = ['author_name']


class EntrySerializer (serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    type = TypeSerializer(many=False)
    color = ColorSerializer(many=False)
    rating = RatingSerializer(many=False)
    user = EntryAuthorSerializer(many=False)

    def get_is_owner(self, obj):

        return self.context['request'].user == obj.user

    class Meta:
        model = Entry
        fields = ['id', 'is_owner', 'user_id', 'whiskey', 'type', 'country', 'part_of_country', 'age_in_years', 'proof', 'color',
                  'mash_bill', 'maturation_details', 'nose', 'palate', 'finish', 'rating', 'notes', 'publication_date', 'image_url', 'published']


class EntryViewSet(viewsets.ViewSet):

    def list(self, request):
        requester_id = request.query_params.get('user_id')

        if requester_id is not None:
            entries = Entry.objects.filter("user_id" == requester_id).all()
        else:
            entries = Entry.objects.all()
        serializer = EntrySerializer(
            entries, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            entry = Entry.objects.get(pk=pk)
            serializer = EntrySerializer(
                entry, many=False, context={'request': request})
            return Response(serializer.data)
        except Entry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
