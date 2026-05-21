from django.db import models


class Exchange(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Exchange"
        verbose_name_plural = "Exchanges"
        ordering = ["name"]


class Asset(models.Model):
    """Represents a digital or fiat asset (e.g., BTC, ETH, BRL)."""

    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.symbol

    class Meta:
        ordering = ["symbol"]


class Market(models.Model):
    """Represents a trading pair (e.g., BTC-BRL) on a specific exchange."""

    exchange = models.ForeignKey(
        Exchange, on_delete=models.CASCADE, related_name="markets"
    )
    base_asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="base_markets"
    )
    quote_asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="quote_markets"
    )

    @property
    def symbol(self) -> str:
        return f"{self.base_asset.symbol}-{self.quote_asset.symbol}"

    def __str__(self) -> str:
        return f"{self.symbol} on {self.exchange.name}"

    class Meta:
        ordering = ["base_asset__symbol", "quote_asset__symbol"]
        unique_together = ("exchange", "base_asset", "quote_asset")


class Ticker(models.Model):
    """Stores real-time and historical ticker data for a market."""

    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="tickers")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    bid_price = models.DecimalField(max_digits=18, decimal_places=8)
    ask_price = models.DecimalField(max_digits=18, decimal_places=8)
    last_price = models.DecimalField(max_digits=18, decimal_places=8)
    volume = models.DecimalField(max_digits=24, decimal_places=8, null=True, blank=True)

    def __str__(self) -> str:
        return f"Ticker for {self.market} at {self.timestamp}"

    class Meta:
        ordering = ["-timestamp"]
        unique_together = ("market", "timestamp")
