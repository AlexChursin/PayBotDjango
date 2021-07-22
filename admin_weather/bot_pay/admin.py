from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

from .models import TableUsers, TableTransactions


# Register your models here.
@admin.register(TableUsers)
class WeatherTypeAdmin(admin.ModelAdmin):
    search_fields = ("telegram_id", 'hash')
    list_display = ("telegram_id", "user_language", "hash",'last_trans', 'last_wallet', 'limits')


@admin.register(TableTransactions)
class TempRangeAdmin(admin.ModelAdmin):
    search_fields = ("telegram_id", "transaction_id", "wallet",)
    list_display = ("telegram_id", "transaction_id", "wallet",)
    # #
    # def view_image_link(self, obj):
    #     count = Image.objects.annotate(temp_range=Count('image'))
    #     return count
    #
    # view_image_link.short_description = "Images"

