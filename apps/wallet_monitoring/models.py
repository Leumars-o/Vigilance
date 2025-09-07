from django.db import models

class BalanceLog(models.Model):
    account = models.ForeignKey(Account)
    calculated_balance = models.DecimalField(max_digits=20, decimal_places=6)
    actual_balance = models.DecimalField(max_digits=20, decimal_places=6)
    discrepancy = models.DecimalField(max_digits=20, decimal_places=6)
    checked_at = models.DateTimeField(auto_now_add=True)

class ManualTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Manual Deposit'),
        ('WITHDRAWAL', 'Manual Withdrawal'),
    ]
    
    account = models.ForeignKey(Account)
    amount = models.DecimalField(max_digits=20, decimal_places=6)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    note = models.TextField()
    recorded_at = models.DateTimeField(auto_now_add=True)
