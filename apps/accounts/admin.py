from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'wallet_address', 'is_active', 'current_streak', 'total_earnings']
    list_filter = ['is_active', 'is_excluded_from_tracking']
    search_fields = ['email', 'wallet_address']
    
