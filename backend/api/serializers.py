from rest_framework import serializers

from bookmarks.models import Bookmark, Collection


class CollectionIdSerializer(serializers.Serializer):
    collection_id = serializers.UUIDField()
    """Идентификатор коллекции (UUID)."""


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


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = [
            'id',
            'created_at',
            'updated_at',
            'title',
            'description',
            'link',
            'link_type',
            'image',
            'collection',
        ]


class BookmarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = [
            'id',
            'created_at',
            'updated_at',
            'title',
            'description',
            'link',
            'link_type',
            'image',
            'collection',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'title',
            'description',
            'link_type',
            'image',
            'collection',
        ]


class DetailSerializer(serializers.Serializer):
    detail = serializers.CharField()


class NotAuthenticatedSerializer(DetailSerializer):
    """HTTP_401."""

    pass


class NotFoundSerializer(DetailSerializer):
    """HTTP_404."""

    pass


class DummySerializer(serializers.Serializer):
    """Заглушка для drf-spectacular, чтобы не ругался ViewSet без сериализаторов."""

    pass
