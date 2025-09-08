from django.contrib import admin
from .models import NotificationRule, Alert


@admin.register(NotificationRule)
class NotificationRuleAdmin(admin.ModelAdmin):
    list_display = ['rule_type', 'is_active', 'threshold_amount', 'description']
    list_filter = ['rule_type', 'is_active']
    search_fields = ['rule_type', 'description']


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['account', 'level', 'message_preview', 'is_read', 'created_at']
    list_filter = ['level', 'is_read', 'created_at', 'rule__rule_type']
    search_fields = ['account__email', 'message']
    readonly_fields = ['created_at']
    
    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'
