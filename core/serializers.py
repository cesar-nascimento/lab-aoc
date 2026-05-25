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
    base_asset = serializers.CharField(source="base_asset.symbol", read_only=True)
    quote_asset = serializers.CharField(source="quote_asset.symbol", read_only=True)
    exchange_name = serializers.CharField(source="exchange.name", read_only=True)

    class Meta:
        model = Market
        fields = [
            "id",
            "exchange",
            "base_asset",
            "quote_asset",
            "symbol",
            "exchange_name",
        ]
        read_only_fields = ("id",)


class TickerSerializer(serializers.ModelSerializer):
    market_symbol = serializers.CharField(source="market.symbol", read_only=True)
    exchange_name = serializers.CharField(source="market.exchange.name", read_only=True)
    base_asset = serializers.CharField(
        source="market.base_asset.symbol", read_only=True
    )
    quote_asset = serializers.CharField(
        source="market.quote_asset.symbol", read_only=True
    )

    class Meta:
        model = Ticker
        fields = [
            "id",
            "market",
            "exchange_name",
            "market_symbol",
            "base_asset",
            "quote_asset",
            "timestamp",
            "bid_price",
            "ask_price",
        ]
        read_only_fields = ["id", "timestamp"]
