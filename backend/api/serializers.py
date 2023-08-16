from rest_framework import serializers

from bookmarks.models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            'id',
            'created_at',
            'updated_at',
            'name',
            'description',
        ]
