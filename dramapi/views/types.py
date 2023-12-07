from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from dramapi.models import Type


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'label']


class TypeViewSet(viewsets.ViewSet):

    def list(self, request):
        types = Type.objects.all()
        serializer = TypeSerializer(types, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            type = Type.objects.get(pk=pk)
            serializer = TypeSerializer(type)
            return Response(serializer.data)
        except Type.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        label = request.data.get('label')

        post = Type.objects.create(label=label)

        serializer = TypeSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            type = Type.objects.get(pk=pk)

            self.check_object_permissions(request, type)

            type.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Type.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
