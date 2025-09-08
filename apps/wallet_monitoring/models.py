# apps/wallet_monitoring/models.py
from django.db import models
from apps.accounts.models import Account


class BalanceLog(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    calculated_balance = models.DecimalField(max_digits=20, decimal_places=6)
    actual_balance = models.DecimalField(max_digits=20, decimal_places=6)
    discrepancy = models.DecimalField(max_digits=20, decimal_places=6)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.account.email} - Balance Check {self.checked_at}"
    
    class Meta:
        db_table = 'wallet_monitoring_balancelog'
        ordering = ['-checked_at']


class ManualTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Manual Deposit'),
        ('WITHDRAWAL', 'Manual Withdrawal'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=6)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    note = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.account.email} - {self.transaction_type} {self.amount}"
    
    class Meta:
        class Meta:
            db_table = 'wallet_monitoring_manualtransaction'
            ordering = ['-recorded_at']
