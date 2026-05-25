from __future__ import annotations

from asgiref.sync import async_to_sync
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Asset, Exchange, Market, Ticker
from core.serializers import (
    AssetSerializer,
    ExchangeSerializer,
    MarketSerializer,
    TickerSerializer,
)
from services.tickers import Exchanges, TickerService

from .filters import TickerFilter


@extend_schema(exclude=True)
class ExternalDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        if request.user.username != "cron_job":
            return Response({"status": "forbidden"}, status=403)

        try:
            async_to_sync(TickerService().run)(exchanges=Exchanges)
            return Response({"status": "ok"})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)


@extend_schema(tags=["Exchanges"])
class ExchangeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=["Assets"])
class AssetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=["Markets"])
class MarketViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Market.objects.select_related(
        "exchange", "base_asset", "quote_asset"
    ).all()
    serializer_class = MarketSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=["Tickers"])
class TickerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ticker.objects.select_related(
        "market",
        "market__exchange",
        "market__base_asset",
        "market__quote_asset",
    ).all()
    serializer_class = TickerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TickerFilter
