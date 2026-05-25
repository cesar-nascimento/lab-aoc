from django.contrib import admin

from .models import Asset, Exchange, Market, Ticker

admin.site.register(Exchange)
admin.site.register(Asset)
admin.site.register(Market)
admin.site.register(Ticker)
