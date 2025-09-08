# apps/wallet_monitoring/services.py
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from apps.accounts.models import Account
from .models import BalanceLog, ManualTransaction
from .blockchain_client import StacksBlockchainClient
import logging

logger = logging.getLogger(__name__)

class WalletMonitoringService:
    """Enhanced wallet monitoring service with Stacks blockchain integration"""
    
    def __init__(self, network='mainnet'):
        self.blockchain_client = StacksBlockchainClient(network=network)
    
    def get_wallet_balance(self, wallet_address: str) -> Optional[Decimal]:
        """Get current balance from Stacks blockchain"""
        try:
            balance = self.blockchain_client.get_stx_balance(wallet_address)
            logger.info(f"Retrieved balance for {wallet_address}: {balance} STX")
            return balance
        except Exception as e:
            logger.error(f"Error getting wallet balance for {wallet_address}: {str(e)}")
            return None
    
    def calculate_expected_balance(self, account: Account) -> Decimal:
        """Calculate expected balance based on submission status and manual transactions"""
        try:
            # Start with 0
            expected_balance = Decimal('0.00')
            
            # Add earnings from submission statuses
            from apps.email_monitoring.models import SubmissionStatus
            earnings = SubmissionStatus.objects.filter(
                account=account,
                status__in=['DRAWN_WON', 'STREAK_PAYOUT'],
                amount__isnull=False
            )
            
            for earning in earnings:
                expected_balance += Decimal(str(earning.amount))
            
            # Add manual deposits and subtract withdrawals
            manual_transactions = ManualTransaction.objects.filter(account=account)
            
            for transaction in manual_transactions:
                if transaction.transaction_type == 'DEPOSIT':
                    expected_balance += transaction.amount
                elif transaction.transaction_type == 'WITHDRAWAL':
                    expected_balance -= transaction.amount
            
            logger.info(f"Calculated expected balance for {account.email}: {expected_balance} STX")
            return expected_balance
            
        except Exception as e:
            logger.error(f"Error calculating expected balance for {account.email}: {str(e)}")
            return Decimal('0.00')
    
    def check_balance_discrepancy(self, account: Account, tolerance: Decimal = Decimal('0.001')) -> Dict:
        """
        Check if actual balance matches calculated balance
        
        Args:
            account: Account to check
            tolerance: Acceptable difference (default 0.001 STX)
            
        Returns:
            Dict with balance info and discrepancy status
        """
        try:
            calculated_balance = self.calculate_expected_balance(account)
            actual_balance = self.get_wallet_balance(account.wallet_address)
            
            if actual_balance is None:
                return {
                    'success': False,
                    'error': 'Could not retrieve actual balance',
                    'calculated_balance': calculated_balance,
                    'actual_balance': None,
                    'discrepancy': None,
                    'has_discrepancy': True
                }
            
            discrepancy = actual_balance - calculated_balance
            has_discrepancy = abs(discrepancy) > tolerance
            
            logger.info(f"Balance check for {account.email}: "
                       f"Calculated: {calculated_balance}, "
                       f"Actual: {actual_balance}, "
                       f"Discrepancy: {discrepancy}")
            
            return {
                'success': True,
                'calculated_balance': calculated_balance,
                'actual_balance': actual_balance,
                'discrepancy': discrepancy,
                'has_discrepancy': has_discrepancy,
                'tolerance': tolerance
            }
            
        except Exception as e:
            logger.error(f"Error checking balance discrepancy for {account.email}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'calculated_balance': None,
                'actual_balance': None,
                'discrepancy': None,
                'has_discrepancy': True
            }
    
    def record_balance_log(self, account: Account, calculated: Decimal, actual: Decimal) -> BalanceLog:
        """Record balance check in database"""
        try:
            discrepancy = actual - calculated if actual is not None else Decimal('0.00')
            
            balance_log = BalanceLog.objects.create(
                account=account,
                calculated_balance=calculated,
                actual_balance=actual or Decimal('0.00'),
                discrepancy=discrepancy
            )
            
            logger.info(f"Recorded balance log for {account.email}: {balance_log.id}")
            return balance_log
            
        except Exception as e:
            logger.error(f"Error recording balance log for {account.email}: {str(e)}")
            raise
    
    def monitor_single_account(self, account: Account) -> Dict:
        """Monitor a single account and record results"""
        try:
            with transaction.atomic():
                balance_check = self.check_balance_discrepancy(account)
                
                if balance_check['success']:
                    # Record the balance log
                    balance_log = self.record_balance_log(
                        account=account,
                        calculated=balance_check['calculated_balance'],
                        actual=balance_check['actual_balance']
                    )
                    
                    # Update account's total earnings if needed
                    if account.total_earnings != balance_check['calculated_balance']:
                        account.total_earnings = balance_check['calculated_balance']
                        account.save(update_fields=['total_earnings'])
                    
                    return {
                        'success': True,
                        'account': account.email,
                        'balance_log_id': balance_log.id,
                        **balance_check
                    }
                else:
                    return {
                        'success': False,
                        'account': account.email,
                        **balance_check
                    }
                    
        except Exception as e:
            logger.error(f"Error monitoring account {account.email}: {str(e)}")
            return {
                'success': False,
                'account': account.email,
                'error': str(e)
            }
    
    def monitor_all_accounts(self, active_only: bool = True) -> Dict:
        """Monitor all accounts and return summary"""
        queryset = Account.objects.all()
        if active_only:
            queryset = queryset.filter(is_active=True, is_excluded_from_tracking=False)
        
        results = {
            'total_checked': 0,
            'successful_checks': 0,
            'failed_checks': 0,
            'accounts_with_discrepancies': 0,
            'details': []
        }
        
        for account in queryset:
            result = self.monitor_single_account(account)
            
            results['total_checked'] += 1
            results['details'].append(result)
            
            if result['success']:
                results['successful_checks'] += 1
                if result.get('has_discrepancy', False):
                    results['accounts_with_discrepancies'] += 1
            else:
                results['failed_checks'] += 1
        
        logger.info(f"Monitoring summary: {results['successful_checks']}/{results['total_checked']} successful")
        return results