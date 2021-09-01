from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(TableUsers)
class TableUsersAdmin(admin.ModelAdmin):
    search_fields = ("telegram_id", 'user_language', 'hash', 'last_trans', 'last_wallet', )
    list_display = ("telegram_id", 'completed', "user_language", "hash", 'last_trans', 'last_wallet', 'limits', 'refer_id', 'from_refer')
    list_filter = ["user_language", "completed"]


@admin.register(TableTransactions)
class TableTransactionsAdmin(admin.ModelAdmin):
    search_fields = ("telegram_id", "transaction_id", "wallet",)
    list_display = ("telegram_id", "transaction_id", "wallet",)


@admin.register(Refer)
class ReferAdmin(admin.ModelAdmin):
    search_fields = ["url"]
    list_display = ("url", "count_refers", "pay_type_id", 'dollars_paid', 'gem_paid',)
    list_filter = ['pay_type_id']

    def count_refers(self, obj):
        return f"{obj.refers.count()}"


@admin.register(PayType)
class PayTypeAdmin(admin.ModelAdmin):
    list_display = ("type", "desc")


admin.site.site_title = 'Администрирование платежного бота'
admin.site.site_header = 'Админ панель бота оплаты'
