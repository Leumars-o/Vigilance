from django.contrib import admin
from .models import NotificationRule, Alert

@admin.register(NotificationRule)
class NotificationRuleAdmin(admin.ModelAdmin):
    list_display = ['rule_type', 'is_active', 'threshold_amount']
    list_filter = ['rule_type', 'is_active']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['account', 'level', 'message', 'is_read', 'created_at']
    list_filter = ['level', 'is_read', 'created_at']
    search_fields = ['account__email', 'message']
