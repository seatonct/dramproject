from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from dramapi.models import Color


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'label', 'color_grade', 'hex_code', 'tailwind_name']


class ColorViewSet(viewsets.ViewSet):

    def list(self, request):
        colors = Color.objects.all()
        serializer = ColorSerializer(colors, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            color = Color.objects.get(pk=pk)
            serializer = ColorSerializer(color)
            return Response(serializer.data)
        except Color.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
