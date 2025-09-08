# apps/accounts/models.py
from django.db import models

class Account(models.Model):
    email = models.EmailField(unique=True)
    wallet_address = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    is_excluded_from_tracking = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    current_streak = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=20, decimal_places=6)


    def __str__(self):
        return f"{self.email} - {self.wallet_address}"
    
    class Meta:
        db_table = 'accounts_account'

