from django.db import models

class Account(models.Model):
    email = models.EmailField(unique=True)
    wallet_address = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    is_excluded_from_tracking = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=0)
    current_streak = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=20, decimal_place=6)
