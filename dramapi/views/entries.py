from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from dramapi.models import Entry, Type, Color, Rating
from .types import TypeSerializer
from .colors import ColorSerializer
from .ratings import RatingSerializer


class EntryAuthorSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    def get_author_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = User
        fields = ['author_name', 'username']


class EntrySerializer (serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    whiskey_type = TypeSerializer(many=False)
    color = ColorSerializer(many=False)
    rating = RatingSerializer(many=False)
    user = EntryAuthorSerializer(many=False)

    def get_is_owner(self, obj):

        return self.context['request'].user == obj.user

    class Meta:
        model = Entry
        fields = ['id', 'is_owner', 'user_id', 'whiskey', 'whiskey_type', 'country', 'part_of_country', 'age_in_years', 'proof', 'color',
                  'mash_bill', 'maturation_details', 'nose', 'palate', 'finish', 'rating', 'notes', 'publication_date', 'user']


class UpdateEntrySerializer (serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ['whiskey', 'whiskey_type', 'country', 'part_of_country', 'age_in_years', 'proof', 'color',
                  'mash_bill', 'maturation_details', 'nose', 'palate', 'finish', 'rating', 'notes']


class EntryViewSet(viewsets.ViewSet):

    def list(self, request):
        username = request.query_params.get('username')
        # bookmark_user = int(request.query_params.get('bookmarkUser'))

        entries = Entry.objects.all().order_by('-publication_date')

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            entries = entries.filter(
                user=user)

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

    def create(self, request):
        whiskey = request.data.get('whiskey')
        whiskey_type = Type.objects.get(pk=request.data['type_id'])
        country = request.data.get('country')
        part_of_country = request.data.get('part_of_country')
        age_in_years = request.data.get('age_in_years')
        proof = request.data.get('proof')
        color = Color.objects.get(pk=request.data['color_id'])
        mash_bill = request.data.get('mash_bill')
        maturation_details = request.data.get('maturation_details')
        nose = request.data.get('nose')
        palate = request.data.get('palate')
        finish = request.data.get('finish')
        rating = Rating.objects.get(pk=request.data['rating_id'])
        notes = request.data.get('notes')

        entry = Entry.objects.create(
            user=request.user,
            whiskey=whiskey,
            whiskey_type=whiskey_type,
            country=country,
            part_of_country=part_of_country,
            age_in_years=age_in_years,
            proof=proof,
            color=color,
            mash_bill=mash_bill,
            maturation_details=maturation_details,
            nose=nose,
            palate=palate,
            finish=finish,
            rating=rating,
            notes=notes
        )

        try:
            serializer = EntrySerializer(
                entry, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            entry = Entry.objects.get(pk=pk)
            self.check_object_permissions(request, entry)
            serializer = UpdateEntrySerializer(data=request.data)

            if serializer.is_valid():
                entry.whiskey = serializer.validated_data['whiskey']
                entry.whiskey_type = Type.objects.get(
                    pk=request.data['whiskey_type'])
                entry.country = serializer.validated_data['country']
                entry.part_of_country = serializer.validated_data['part_of_country']
                entry.age_in_years = serializer.validated_data['age_in_years']
                entry.proof = serializer.validated_data['proof']
                entry.color = Color.objects.get(pk=request.data['color_id'])
                entry.mash_bill = serializer.validated_data['mash_bill']
                entry.maturation_details = serializer.validated_data['maturation_details']
                entry.nose = serializer.validated_data['nose']
                entry.palate = serializer.validated_data['palate']
                entry.finish = serializer.validated_data['finish']
                entry.rating = Rating.objects.get(
                    pk=request.data['rating'])
                entry.notes = serializer.validated_data['notes']
                entry.save()

                serializer = UpdateEntrySerializer(
                    entry, context={'request': request})
                return Response(None, status.HTTP_202_ACCEPTED)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Entry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            entry = Entry.objects.get(pk=pk)

            if entry.user_id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            entry.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Entry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
