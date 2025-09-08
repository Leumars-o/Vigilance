from django.contrib import admin
from .models import EmailAccount, EmailLog, SubmissionStatus


@admin.register(EmailAccount)
class EmailAccountAdmin(admin.ModelAdmin):
    list_display = ['account', 'email_provider', 'last_checked']
    list_filter = ['email_provider']
    search_fields = ['account__email']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['account', 'subject', 'sender', 'processed_at']
    list_filter = ['processed_at', 'sender']
    search_fields = ['account__email', 'subject', 'sender']
    readonly_fields = ['content_hash', 'processed_at']


@admin.register(SubmissionStatus)
class SubmissionStatusAdmin(admin.ModelAdmin):
    list_display = ['account', 'status', 'amount', 'submission_date']
    list_filter = ['status', 'submission_date']
    search_fields = ['account__email']

