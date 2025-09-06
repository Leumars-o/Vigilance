from django.db import models

class EmailAccount(models.Model):
    account = models.OneToOneField(Account)
    email_provider = models.CharField(max_length=50)
    last_checked = models.DateTimeField()
    credentials_encrypted = models.TextField() # Encrypted access tokens

class EmailLog(models.Model):
    account = models.ForeignKey(Account)
    subject = models.TextField()
    sender = models.EmailField()
    receiver = models.EmailField()
    fowarded_from = models.EmailField(null=True) # Edge case handling
    content_hash = models.CharField(max_length=64) # prevent duplicate
    raw_headers = models.JSONField()
    processed_at = models.DateTimeField(auto_now_add=True)

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

    account = models.ForeignKey(Account)
    email_log = models.ForeignObjectRel(EmailLog)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    amount = models.IntegerField(null=True, choices=AMOUNT_CHOICES)
    submission_date = models.DateTimeField()


