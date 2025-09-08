# apps/wallet_monitoring/blockchain_client.py
import requests
import logging
from decimal import Decimal
from typing import Optional, Dict, Any
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class StacksBlockchainClient:
    """Client for interacting with Stacks blockchain API"""
    
    # API endpoints
    MAINNET_API = "https://api.mainnet.hiro.so"
    TESTNET_API = "https://api.testnet.hiro.so"
    
    # STX has 6 decimal places (micro-STX)
    STX_DECIMALS = 6
    MICRO_STX_MULTIPLIER = 10 ** STX_DECIMALS
    
    def __init__(self, network='mainnet', timeout=30, cache_duration=300):
        """
        Initialize Stacks client
        
        Args:
            network: 'mainnet' or 'testnet'
            timeout: Request timeout in seconds
            cache_duration: Cache duration in seconds
        """
        if network not in ['mainnet', 'testnet']:
            raise ValueError("Network must be 'mainnet' or 'testnet'")
        
        self.network = network
        self.base_url = self.MAINNET_API if network == 'mainnet' else self.TESTNET_API
        self.timeout = timeout
        self.cache_duration = cache_duration
    
    def _make_request(self, endpoint: str, use_cache: bool = True) -> Optional[Dict[Any, Any]]:
        """
        Make API request with error handling and optional caching
        """
        url = f"{self.base_url}{endpoint}"
        cache_key = f"stacks_api_{self.network}_{endpoint.replace('/', '_')}"
        
        # Try cache first if enabled
        if use_cache:
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_result
        
        try:
            logger.debug(f"Making request to: {url}")
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                # Cache successful responses
                if use_cache:
                    cache.set(cache_key, data, self.cache_duration)
                
                return data
            else:
                logger.warning(f"API request failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout while requesting {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {str(e)}")
            return None
        except ValueError as e:
            logger.error(f"JSON decode error for {url}: {str(e)}")
            return None
    
    def get_stx_balance(self, address: str, use_cache: bool = True) -> Optional[Decimal]:
        """
        Get STX balance for an address
        
        Args:
            address: Stacks wallet address
            use_cache: Whether to use cached results
            
        Returns:
            Decimal balance in STX or None if error
        """
        endpoint = f"/extended/v1/address/{address}/balances"
        data = self._make_request(endpoint, use_cache)
        
        if data and 'stx' in data and 'balance' in data['stx']:
            # Convert micro-STX to STX
            micro_stx_balance = int(data['stx']['balance'])
            stx_balance = Decimal(micro_stx_balance) / Decimal(self.MICRO_STX_MULTIPLIER)
            return stx_balance
        
        return None
    
    def get_address_info(self, address: str, use_cache: bool = True) -> Optional[Dict[Any, Any]]:
        """
        Get comprehensive address information
        
        Returns:
            Dict with balance, locked, unlock_height, etc.
        """
        endpoint = f"/extended/v1/address/{address}/balances"
        data = self._make_request(endpoint, use_cache)
        
        if data and 'stx' in data:
            stx_data = data['stx']
            return {
                'balance': Decimal(int(stx_data['balance'])) / Decimal(self.MICRO_STX_MULTIPLIER),
                'locked': Decimal(int(stx_data.get('locked', 0))) / Decimal(self.MICRO_STX_MULTIPLIER),
                'unlock_height': stx_data.get('unlock_height', 0),
                'total_sent': Decimal(int(stx_data.get('total_sent', 0))) / Decimal(self.MICRO_STX_MULTIPLIER),
                'total_received': Decimal(int(stx_data.get('total_received', 0))) / Decimal(self.MICRO_STX_MULTIPLIER),
                'total_fees_sent': Decimal(int(stx_data.get('total_fees_sent', 0))) / Decimal(self.MICRO_STX_MULTIPLIER),
            }
        
        return None
    
    def get_recent_transactions(self, address: str, limit: int = 50) -> Optional[list]:
        """
        Get recent transactions for an address
        """
        endpoint = f"/extended/v1/address/{address}/transactions?limit={limit}"
        data = self._make_request(endpoint, use_cache=False)  # Don't cache transactions
        
        if data and 'results' in data:
            return data['results']
        
        return None
    
    def validate_address(self, address: str) -> bool:
        """
        Validate address by checking if it exists on blockchain
        """
        try:
            result = self.get_stx_balance(address, use_cache=False)
            return result is not None
        except Exception:
            return False