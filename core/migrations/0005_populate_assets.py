from typing import Any

from django.db import migrations

CURRENCIES_DATA = [
    {"name": "Bitcoin", "symbol": "btc"},
    {"name": "Ethereum", "symbol": "eth"},
    {"name": "XRP", "symbol": "xrp"},
    {"name": "Solana", "symbol": "sol"},
    {"name": "BNB", "symbol": "bnb"},
    {"name": "Cardano", "symbol": "ada"},
    {"name": "Dogecoin", "symbol": "doge"},
    {"name": "Avalanche", "symbol": "avax"},
    {"name": "Polkadot", "symbol": "dot"},
    {"name": "Chainlink", "symbol": "link"},
    {"name": "Litecoin", "symbol": "ltc"},
    {"name": "Tether", "symbol": "usdt"},
    {"name": "USD Coin", "symbol": "usdc"},
    {"name": "Tron", "symbol": "trx"},
    {"name": "Stellar", "symbol": "xlm"},
    {"name": "Bitcoin Cash", "symbol": "bch"},
    {"name": "Algorand", "symbol": "algo"},
    {"name": "Shiba Inu", "symbol": "shib"},
    {"name": "Toncoin", "symbol": "ton"},
    {"name": "Hedera", "symbol": "hbar"},
    {"name": "Cosmos", "symbol": "atom"},
    {"name": "Near", "symbol": "near"},
    {"name": "Sui", "symbol": "sui"},
    {"name": "Arbitrum", "symbol": "arb"},
    {"name": "Optimism", "symbol": "op"},
    {"name": "Injective", "symbol": "inj"},
    {"name": "Uniswap", "symbol": "uni"},
    {"name": "Aave", "symbol": "aave"},
    {"name": "Maker", "symbol": "mkr"},
    {"name": "Synthetix", "symbol": "snx"},
]


def populate_assets(apps: Any, schema_editor: Any) -> None:
    """Populates the Asset table with the initial currency data."""
    Asset = apps.get_model("core", "Asset")
    assets_to_create = [
        Asset(name=currency["name"], symbol=currency["symbol"].upper())
        for currency in CURRENCIES_DATA
    ]
    Asset.objects.bulk_create(assets_to_create, ignore_conflicts=True)


def unpopulate_assets(apps: Any, schema_editor: Any) -> None:
    """Deletes the assets that were added by this migration."""
    Asset = apps.get_model("core", "Asset")
    symbols = [currency["symbol"].upper() for currency in CURRENCIES_DATA]
    Asset.objects.filter(symbol__in=symbols).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_alter_market_options_remove_market_symbol"),
    ]

    operations = [
        migrations.RunPython(populate_assets, reverse_code=unpopulate_assets),
    ]
