from django.contrib import admin
from .models import EmailAccount, EmailLog, SubmissionStatus


@admin.register(EmailAccount)
class EmailAccountAdmin(admin.ModelAdmin):
    list_display = ['account', 'email_provider', 'last_checked']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['account', 'status', 'amount', 'submission_date']
    list_filter = ['status', 'submission_date']
    

