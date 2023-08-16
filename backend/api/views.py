from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, viewsets

from api.serializers import CollectionSerializer
from bookmarks.models import Collection

User = get_user_model()


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        """Use this endpoint to register user."""
        return super().create(request, *args, **kwargs)

    class Meta:
        model = User


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
