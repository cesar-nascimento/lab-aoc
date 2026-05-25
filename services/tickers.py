from __future__ import annotations

import asyncio
import logging
import os
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Type, TypedDict

import django
import niquests
from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab_aoc_django_backend.settings")
django.setup()

from core import models  # noqa: E402, I001


logger = logging.getLogger(__name__)


class TickerData(TypedDict):
    base_asset: str
    quote_asset: str
    bid_price: Decimal
    ask_price: Decimal


class Exchange(ABC):
    @abstractmethod
    async def get_tickers(self) -> list[TickerData]:
        pass

    @property
    @abstractmethod
    def base_url(self) -> str:
        pass

    @property
    @abstractmethod
    def exchange_name(self) -> str:
        pass


class Binance(Exchange):
    base_url = "https://api.binance.us/api/v3"
    exchange_name = "Binance"

    async def get_tickers(self) -> list[TickerData]:
        logger.info("Fetching tickers from %s", self.exchange_name)
        async with niquests.AsyncSession(base_url=self.base_url) as session:
            markets = await session.get("/exchangeInfo")
            symbols = {
                symbol["symbol"]: {
                    "base_asset": symbol["baseAsset"],
                    "quote_asset": symbol["quoteAsset"],
                }
                for symbol in markets.json()["symbols"]
            }
            tickers = await session.get("/ticker/bookTicker")
            ticker_data = [
                TickerData(
                    base_asset=symbols[tickers["symbol"]]["base_asset"],
                    quote_asset=symbols[tickers["symbol"]]["quote_asset"],
                    bid_price=Decimal(str(tickers["bidPrice"])),
                    ask_price=Decimal(str(tickers["askPrice"])),
                )
                for tickers in tickers.json()
            ]
        logger.info("Fetched %d tickers from %s", len(ticker_data), self.exchange_name)
        return ticker_data


class Foxbit(Exchange):
    base_url = "https://api.foxbit.com.br/rest/v3"
    exchange_name = "Foxbit"

    async def get_tickers(self) -> list[TickerData]:
        logger.info("Fetching tickers from %s", self.exchange_name)
        async with niquests.AsyncSession(base_url=self.base_url) as session:
            markets = await session.get("/markets")
            symbols = {
                symbol["symbol"]: {
                    "base_asset": symbol["base"]["symbol"],
                    "quote_asset": symbol["quote"]["symbol"],
                }
                for symbol in markets.json()["data"]
            }
            tickers = await session.get("/markets/ticker/24hr")
            ticker_data = [
                TickerData(
                    base_asset=symbols[tickers["market_symbol"]]["base_asset"].upper(),
                    quote_asset=symbols[tickers["market_symbol"]][
                        "quote_asset"
                    ].upper(),
                    bid_price=Decimal(str(tickers["best"]["bid"]["price"])),
                    ask_price=Decimal(str(tickers["best"]["ask"]["price"])),
                )
                for tickers in tickers.json()["data"]
            ]
        logger.info("Fetched %d tickers from %s", len(ticker_data), self.exchange_name)
        return ticker_data


class TickerService:
    async def get_tickers(self, exchange_class: Type[Exchange]) -> None:
        exchange: Exchange = exchange_class()
        logger.info("Start sync for exchange %s", exchange.exchange_name)

        market_map: dict[tuple, models.Market] = await sync_to_async(
            self.get_known_markets
        )(exchange_name=exchange.exchange_name)

        raw_tickers: list[TickerData] = await exchange.get_tickers()
        filtered_tickers = [
            models.Ticker(
                market=market_map[(ticker["base_asset"], ticker["quote_asset"])],
                bid_price=ticker["bid_price"],
                ask_price=ticker["ask_price"],
            )
            for ticker in raw_tickers
            if (ticker["base_asset"], ticker["quote_asset"]) in market_map
        ]
        logger.info(
            "Filtered %d/%d tickers for exchange %s",
            len(filtered_tickers),
            len(raw_tickers),
            exchange.exchange_name,
        )
        await sync_to_async(models.Ticker.objects.bulk_create)(filtered_tickers)
        logger.info(
            "Saved %d tickers for exchange %s",
            len(filtered_tickers),
            exchange.exchange_name,
        )

    def get_known_markets(self, exchange_name: str) -> dict[tuple, models.Market]:
        logger.debug("Loading known markets for %s", exchange_name)
        markets = models.Market.objects.filter(
            exchange__name=exchange_name
        ).select_related("base_asset", "quote_asset")
        market_map = {(m.base_asset.symbol, m.quote_asset.symbol): m for m in markets}
        logger.debug("Loaded %d known markets for %s", len(market_map), exchange_name)
        return market_map

    async def run(self, exchanges: list[Type[Exchange]]) -> None:
        await asyncio.gather(*(self.get_tickers(exchange) for exchange in exchanges))


Exchanges = [Foxbit, Binance]


async def main() -> None:
    await TickerService().run(exchanges=Exchanges)


if __name__ == "__main__":
    asyncio.run(main())
