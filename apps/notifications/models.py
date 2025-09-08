from django.db import models
from apps.accounts.models import Account

class NotificationRule(models.Model):
    RULE_TYPES = [
        ('BALANCE_DISCREPANCY', 'Balance Discrepancy'),
        ('SUBMISSION_REJECTED', 'Submisson Rejected'),
        ('RAFFLE_WON', 'Raffle Won'),
        ('STREAK_BROKEN', 'Streak Broken'),
        ('STREAK_PAYOUT', 'Streak Payout'),
    ]

    rule_type = models.CharField(max_length=30, choices=RULE_TYPES)
    is_active = models.BooleanField(default=True)
    threshold_amount = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.rule_type} - {'Active' if self.is_active else 'Inactive'}"
    
    class Meta:
        db_table = 'notifications_notificationrule'


class Alert(models.Model):
    ALERT_LEVELS = [
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('SUCCESS', 'Success'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    rule = models.ForeignKey(NotificationRule, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=ALERT_LEVELS)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.account.email} - {self.level}: {self.message[:50]}"
    
    class Meta:
        db_table = 'notifications_alert'
        ordering = ['-created_at']