from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import mixins, viewsets

User = get_user_model()


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        """Use this endpoint to register user."""
        return super().create(request, *args, **kwargs)

    class Meta:
        model = User
