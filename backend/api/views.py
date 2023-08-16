from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import decorators, mixins, permissions, status, viewsets
from rest_framework.response import Response

from api import schema
from api.serializers import (
    BookmarkCreateSerializer,
    BookmarkSerializer,
    CollectionSerializer,
    DummySerializer,
)
from bookmarks.models import Bookmark, Collection
from bookmarks.services import fill_bookmark_by_link

User = get_user_model()


@extend_schema_view(**schema.TOKEN_CREATE_VIEW_SCHEMA)
class TokenCreateView(DjoserTokenCreateView):
    pass


@extend_schema_view(**schema.TOKEN_DESTROY_VIEW_SCHEMA)
class TokenDestroyView(DjoserTokenDestroyView):
    serializer_class = DummySerializer


@extend_schema_view(**schema.USER_VIEW_SET_SCHEMA)
class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        """Use this endpoint to register user."""
        return super().create(request, *args, **kwargs)

    class Meta:
        model = User


@extend_schema_view(**schema.COLLECTION_VIEW_SET_SCHEMA)
class CollectionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CollectionSerializer

    class Meta:
        model = Collection

    def get_queryset(self):
        return self.request.user.collections

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(**schema.BOOKMARK_VIEW_SET_SCHEMA)
class BookmarkViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    permission_classes = (permissions.IsAuthenticated,)

    class Meta:
        model = Bookmark

    def get_serializer_class(self):
        if self.action == 'create':
            return BookmarkCreateSerializer
        return BookmarkSerializer

    def get_queryset(self):
        return self.request.user.bookmarks

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance = fill_bookmark_by_link(serializer.validated_data['link'])
        kwargs = {
            'user': self.request.user,
            'title': instance.title,
            'description': instance.description,
            'link_type': instance.link_type,
            'image': instance.image,
        }
        serializer.save(**kwargs)

    def _set_collection(self, request, collection_id=None):
        if collection_id:
            get_object_or_404(request.user.collections, id=collection_id)
        instance = self.get_object()
        instance.collection_id = collection_id
        instance.save(update_fields=('collection_id',))
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @decorators.action(
        methods=['post'],
        detail=True,
    )
    def collection(self, request, pk):
        collection_id = request.data.get('collection_id')
        return self._set_collection(request, collection_id)

    @decorators.action(
        methods=['delete'],
        detail=True,
        url_path='collection',
    )
    def collection_delete(self, request, pk):
        return self._set_collection(request)
