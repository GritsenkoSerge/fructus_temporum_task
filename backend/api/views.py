from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser import serializers as djoser_serializers
from djoser.serializers import UserCreateSerializer
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import decorators, mixins, permissions, status, viewsets
from rest_framework.response import Response

from api.serializers import (
    BookmarkCreateSerializer,
    BookmarkSerializer,
    CollectionIdSerializer,
    CollectionSerializer,
    DummySerializer,
    NotAuthenticatedSerializer,
)
from bookmarks.models import Bookmark, Collection
from bookmarks.services import fill_bookmark_by_link

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        summary='Авторизовать пользователя.',
        description='При успешной авторизации возвращается токен.',
        responses={
            status.HTTP_200_OK: djoser_serializers.TokenSerializer,
        },
        examples=[
            OpenApiExample(
                'Example',
                request_only=True,
                value={'email': 'user@example.com', 'password': 'string'},
            ),
        ],
    ),
)
class TokenCreateView(DjoserTokenCreateView):
    pass


@extend_schema_view(
    post=extend_schema(
        summary='Отозвать авторизацию пользователя.',
        description='При успешном отзыве авторизацию удаляется токен.',
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
)
class TokenDestroyView(DjoserTokenDestroyView):
    serializer_class = DummySerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        """Use this endpoint to register user."""
        return super().create(request, *args, **kwargs)

    class Meta:
        model = User


@extend_schema_view(
    retrieve=extend_schema(
        summary='Получить информацию о коллекции.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор коллекции (UUID).',
            ),
        ],
    ),
    destroy=extend_schema(
        summary='Удалить коллекцию.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор коллекции (UUID).',
            ),
        ],
    ),
    partial_update=extend_schema(
        summary='Изменить коллекцию.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор коллекции (UUID).',
            ),
        ],
    ),
)
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


@extend_schema_view(
    collection=extend_schema(
        summary='Добавить закладку в коллекцию.',
        request=CollectionIdSerializer,
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор закладки (UUID).',
            ),
        ],
        responses={
            status.HTTP_201_CREATED: BookmarkSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    collection_delete=extend_schema(
        summary='Удалить закладку из коллекции.',
        description=(
            'Данный эндпоинт НЕ удаляет саму закладку. '
            'В результате выполнения закладка становится с незаданной коллекцией.'
        ),
        request=None,
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор закладки (UUID).',
            ),
        ],
        responses={
            status.HTTP_200_OK: BookmarkSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    retrieve=extend_schema(
        summary='Получить информацию о закладке.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор закладки (UUID).',
            ),
        ],
    ),
    destroy=extend_schema(
        summary='Удалить закладку.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор закладки (UUID).',
            ),
        ],
    ),
)
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
