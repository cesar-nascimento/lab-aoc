from __future__ import annotations

from django.contrib.auth.models import Group, User
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets

from core.models import Exchange
from core.serializers import ExchangeSerializer, GroupSerializer, UserSerializer


@extend_schema(tags=["Users"])
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=["Groups"])
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=["Exchanges"])
class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]
