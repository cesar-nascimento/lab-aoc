import django_filters
from django.db.models import QuerySet

from core.models import Ticker


class TickerFilter(django_filters.FilterSet):
    exchange = django_filters.CharFilter(
        field_name="market__exchange__name", lookup_expr="iexact"
    )

    symbol = django_filters.CharFilter(method="filter_by_symbol")

    class Meta:
        model = Ticker

        fields = {
            "timestamp": ["exact", "gte", "lte"],
        }

    def filter_by_symbol(
        self, queryset: QuerySet[Ticker], _name: str, value: str
    ) -> QuerySet[Ticker]:
        """
        Splits the requested symbol (e.g., 'BTC-BRL') and queries
        the underlying foreign key relationships.
        """
        try:
            base_symbol, quote_symbol = value.split("-")

            return queryset.filter(
                market__base_asset__symbol__iexact=base_symbol,
                market__quote_asset__symbol__iexact=quote_symbol,
            )
        except ValueError:
            return queryset.none()
