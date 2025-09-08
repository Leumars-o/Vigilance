from django.contrib import admin
from .models import BalanceLog, ManualTransaction


@admin.register(BalanceLog)
class BalanceLogAdmin(admin.ModelAdmin):
    list_display = ['account', 'calculated_balance', 'actual_balance', 'discrepancy', 'checked_at']
    list_filter = ['checked_at']
    search_fields = ['account__email']
    readonly_fields = ['checked_at']

@admin.register(ManualTransaction)
class ManualTransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'transaction_type', 'amount', 'recorded_at']
    list_filter = ['transaction_type', 'recorded_at']
    search_fields = ['account__email']
    readonly_fields = ['recorded_at']