from rest_framework import serializers

from core.models import Asset, Exchange, Market, Ticker


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ["name"]


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["id", "symbol", "name"]


class MarketSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(read_only=True)

    class Meta:
        model = Market
        fields = ["id", "exchange", "base_asset", "quote_asset", "symbol"]
        read_only_fields = ("id",)


class TickerSerializer(serializers.ModelSerializer):
    market_symbol = serializers.CharField(source="market.symbol", read_only=True)

    class Meta:
        model = Ticker
        fields = [
            "id",
            "market_symbol",
            "market",
            "timestamp",
            "bid_price",
            "ask_price",
        ]
        read_only_fields = ["id", "timestamp"]
