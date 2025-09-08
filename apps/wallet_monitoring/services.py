# apps/wallet_monitoring/services.py
from apps.accounts.models import Account
from .models import BalanceLog, ManualTransaction


class WalletMonitoringService:
    @staticmethod
    def get_wallet_balance(wallet_address):
        """Get current balance from blockchain"""
        pass
    
    @staticmethod
    def calculate_expected_balance(account):
        """Calculate expected balance based on status and manual transactions"""
        pass
    
    @staticmethod
    def check_balance_discrepancy(account):
        """Check if actual balance matches calculated balance"""
        pass

    @staticmethod
    def record_balance_log(account, calculated, actual):
        """Record balance check in db"""
        pass
