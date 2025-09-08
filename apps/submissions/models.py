from django.db import models
from apps.accounts.models import Account

class Submission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TimeField()
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self) -> str:
        return f"{self.account.email} - {self.title}"
    
    class Meta:
        db_table = 'submissions_submission'
        ordering = ['-submission_date']


class RaffleResult(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    won = models.BooleanField(default=False)
    amount_won = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    raffle_date = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.account.email} - {'Won' if self.won else 'Lost'}"
    
    class Meta:
        db_table = 'submissions_raffleresult'
        ordering = ['-raffle_date']


class StreakRecord(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    streak_count = models.IntegerField()
    streak_date = models.DateTimeField()
    payout_amount = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.account.email} - Streak {self.streak_count}"
    
    class Meta:
        db_table = 'submissions_streakrecord'
        ordering = ['-streak_date']