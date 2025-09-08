# apps/email_monitoring/models.py
from django.db import models
from apps.accounts.models import Account

class EmailAccount(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    email_provider = models.CharField(max_length=50)
    last_checked = models.DateTimeField()
    credentials_encrypted = models.TextField() # Encrypted access tokens

    def __str__(self) -> str:
        return f"{self.account.email} - {self.email_provider}"
    
    class Meta:
        db_table = 'email_monitoring_emailaccount'


class EmailLog(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.TextField()
    sender = models.EmailField()
    receiver = models.EmailField()
    forwarded_from = models.EmailField(null=True, blank=True) # Edge case handling
    content_hash = models.CharField(max_length=64) # prevent duplicate
    raw_headers = models.JSONField()
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.account.email} - {self.subject[:50]}"
    
    class Meta:
        db_table = 'email_monitoring_emaillog'
        unique_together = ['account', 'content_hash']


class SubmissionStatus(models.Model):
    STATUS_CHOICES = [
        ('SELECTED_NOT_DRAWN', 'Selected but not drawn'),
        ('DRAWN_WON', 'Drawn and won'),
        ('REJECTED', 'Rejected'),
        ('STREAK_PAYOUT', 'Streak payout'),
    ]

    AMOUNT_CHOICES = [
        (10, '10 STX'),
        (15, '15 STX'),
        (30, '30 STX'),
        (100, '100 STX'),
        (200, '200 STX'),
        (500, '500 STX'),
        (2500, '2500 STX'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    email_log = models.ForeignObjectRel(EmailLog, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    amount = models.IntegerField(null=True, blank=True, choices=AMOUNT_CHOICES)
    submission_date = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.account.email} - {self.status}"
    
    class Meta:
        db_table = 'email_monitoring_submissionstatus'

