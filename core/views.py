from __future__ import annotations

from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import mixins, permissions, viewsets

from core.models import Asset, Exchange, Market, Ticker
from core.serializers import (
    AssetSerializer,
    ExchangeSerializer,
    MarketSerializer,
    TickerSerializer,
)


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
    queryset = Market.objects.all()
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
                "last_price": "350025.00",
                "volume": "10.50000000",
            },
            response_only=True,
        ),
    ],
)
class TickerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    permission_classes = [permissions.IsAuthenticated]
