# apps/wallet_monitoring/management/commands/monitor_wallets.py
from django.core.management.base import BaseCommand, CommandError
from apps.accounts.models import Account
from apps.wallet_monitoring.services import WalletMonitoringService
import json

class Command(BaseCommand):
    help = 'Monitor wallet balances for all accounts'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--network',
            type=str,
            default='mainnet',
            choices=['mainnet', 'testnet'],
            help='Stacks network to use (default: mainnet)'
        )
        parser.add_argument(
            '--account-id',
            type=int,
            help='Monitor specific account ID only'
        )
        parser.add_argument(
            '--include-inactive',
            action='store_true',
            help='Include inactive accounts in monitoring'
        )
        parser.add_argument(
            '--format',
            type=str,
            default='table',
            choices=['table', 'json'],
            help='Output format (default: table)'
        )
    
    def handle(self, *args, **options):
        network = options['network']
        account_id = options['account_id']
        include_inactive = options['include_inactive']
        output_format = options['format']
        
        service = WalletMonitoringService(network=network)
        
        try:
            if account_id:
                # Monitor specific account
                try:
                    account = Account.objects.get(id=account_id)
                    result = service.monitor_single_account(account)
                    
                    if output_format == 'json':
                        self.stdout.write(json.dumps(result, indent=2, default=str))
                    else:
                        self.display_single_result(result)
                        
                except Account.DoesNotExist:
                    raise CommandError(f'Account with ID {account_id} does not exist')
            else:
                # Monitor all accounts
                results = service.monitor_all_accounts(active_only=not include_inactive)
                
                if output_format == 'json':
                    self.stdout.write(json.dumps(results, indent=2, default=str))
                else:
                    self.display_summary_results(results)
                    
        except Exception as e:
            raise CommandError(f'Error during monitoring: {str(e)}')
    
    def display_single_result(self, result):
        """Display single account result in table format"""
        self.stdout.write(f"\n=== Account: {result['account']} ===")
        
        if result['success']:
            self.stdout.write(f"Calculated Balance: {result['calculated_balance']} STX")
            self.stdout.write(f"Actual Balance: {result['actual_balance']} STX")
            self.stdout.write(f"Discrepancy: {result['discrepancy']} STX")
            
            if result['has_discrepancy']:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  DISCREPANCY DETECTED!")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS("✅ Balance matches expected")
                )
        else:
            self.stdout.write(
                self.style.ERROR(f"❌ Error: {result.get('error', 'Unknown error')}")
            )
    
    def display_summary_results(self, results):
        """Display summary results in table format"""
        self.stdout.write(f"\n=== Wallet Monitoring Summary ===")
        self.stdout.write(f"Total Accounts Checked: {results['total_checked']}")
        self.stdout.write(f"Successful Checks: {results['successful_checks']}")
        self.stdout.write(f"Failed Checks: {results['failed_checks']}")
        self.stdout.write(f"Accounts with Discrepancies: {results['accounts_with_discrepancies']}")
        
        if results['accounts_with_discrepancies'] > 0:
            self.stdout.write(self.style.WARNING("\n⚠️  Accounts with discrepancies:"))
            for detail in results['details']:
                if detail.get('success') and detail.get('has_discrepancy'):
                    self.stdout.write(f"  - {detail['account']}: {detail['discrepancy']} STX")
        
        if results['failed_checks'] > 0:
            self.stdout.write(self.style.ERROR("\n❌ Failed checks:"))
            for detail in results['details']:
                if not detail.get('success'):
                    self.stdout.write(f"  - {detail['account']}: {detail.get('error', 'Unknown error')}")
