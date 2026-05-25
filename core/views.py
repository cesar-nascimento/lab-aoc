from __future__ import annotations

from asgiref.sync import async_to_sync
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiExample, extend_schema
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


@extend_schema(
    tags=["Exchanges"],
    examples=[
        OpenApiExample(
            "Example Exchange List",
            value=[
                {"name": "Binance"},
                {"name": "Mercado Bitcoin"},
            ],
            response_only=True,
        )
    ],
)
class ExchangeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    tags=["Assets"],
    examples=[
        OpenApiExample(
            "Example Asset List",
            value=[
                {
                    "url": "/api/assets/1/",
                    "id": 1,
                    "symbol": "BTC",
                    "name": "Bitcoin",
                },
                {
                    "url": "/api/assets/2/",
                    "id": 2,
                    "symbol": "BRL",
                    "name": "Brazilian Real",
                },
            ],
            response_only=True,
        )
    ],
)
class AssetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    tags=["Markets"],
    examples=[
        OpenApiExample(
            "Example Market List",
            value=[
                {
                    "url": "/api/markets/1/",
                    "id": 1,
                    "exchange": 1,
                    "base_asset": 1,
                    "quote_asset": 2,
                    "symbol": "BTC-BRL",
                }
            ],
            response_only=True,
        )
    ],
)
class MarketViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Market.objects.select_related(
        "exchange", "base_asset", "quote_asset"
    ).all()
    serializer_class = MarketSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    tags=["Tickers"],
    examples=[
        OpenApiExample(
            "Example Ticker Response",
            value={
                "url": "/api/tickers/1/",
                "id": 1,
                "market_symbol": "BTC-BRL",
                "market": 1,
                "timestamp": "2024-05-21T14:15:22Z",
                "bid_price": "350000.00",
                "ask_price": "350050.00",
            },
            response_only=True,
        ),
    ],
)
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
