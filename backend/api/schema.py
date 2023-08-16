from djoser import serializers as djoser_serializers
from djoser.serializers import UserCreateSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status

from api.serializers import (
    BookmarkCreateSerializer,
    BookmarkSerializer,
    CollectionIdSerializer,
    CollectionSerializer,
    NotAuthenticatedSerializer,
    NotFoundSerializer,
    ValidationSerializer,
)

TOKEN_CREATE_VIEW_SCHEMA = {
    'post': extend_schema(
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
}

TOKEN_DESTROY_VIEW_SCHEMA = {
    'post': extend_schema(
        summary='Отозвать авторизацию пользователя.',
        description='При успешном отзыве авторизацию удаляется токен.',
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
}

USER_VIEW_SET_SCHEMA = {
    'create': extend_schema(
        summary='Зарегистрировать пользователя.',
        responses={
            status.HTTP_201_CREATED: UserCreateSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
        },
    ),
}

COLLECTION_VIEW_SET_SCHEMA = {
    'list': extend_schema(
        summary='Получить список коллекций.',
        responses={
            status.HTTP_200_OK: CollectionSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    'create': extend_schema(
        summary='Создать коллекцию.',
        responses={
            status.HTTP_201_CREATED: CollectionSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    'retrieve': extend_schema(
        summary='Получить информацию о коллекции.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор коллекции (UUID).',
            ),
        ],
        responses={
            status.HTTP_200_OK: CollectionSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    ),
    'destroy': extend_schema(
        summary='Удалить коллекцию.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор коллекции (UUID).',
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    ),
    'partial_update': extend_schema(
        summary='Изменить коллекцию.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор коллекции (UUID).',
            ),
        ],
        responses={
            status.HTTP_200_OK: CollectionSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    ),
}

BOOKMARK_VIEW_SET_SCHEMA = {
    'list': extend_schema(
        summary='Получить список закладок.',
        responses={
            status.HTTP_200_OK: BookmarkSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    'create': extend_schema(
        summary='Создать закладку.',
        responses={
            status.HTTP_201_CREATED: BookmarkCreateSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    'collection': extend_schema(
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
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    ),
    'collection_delete': extend_schema(
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
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    ),
    'retrieve': extend_schema(
        summary='Получить информацию о закладке.',
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
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    ),
    'destroy': extend_schema(
        summary='Удалить закладку.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор закладки (UUID).',
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    ),
}
