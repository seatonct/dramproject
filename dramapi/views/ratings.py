from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from dramapi.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'number_rating', 'label']


class RatingViewSet(viewsets.ViewSet):

    def list(self, request):
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating)
            return Response(serializer.data)
        except Rating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
