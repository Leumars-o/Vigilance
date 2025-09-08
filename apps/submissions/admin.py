from django.contrib import admin
from .models import Submission, RaffleResult, StreakRecord

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['account', 'title', 'status', 'submission_date']
    list_filter = ['status', 'submission_date']
    search_fields = ['account__email', 'title']


@admin.register(RaffleResult)
class RaffleResultAdmin(admin.ModelAdmin):
    list_display = ['account', 'won', 'amount_won', 'raffle_date']
    list_filter = ['won', 'raffle_date']


@admin.register(StreakRecord)
class StreakRecordAdmin(admin.ModelAdmin):
    list_display = ['account', 'streak_count', 'payout_amount', 'streak_date']
    list_filter = ['streak_date']