from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    """Full account serilizer for detailed views"""
    class Meta:
        model = Account
        fields = [
            'id', 'email', 'wallet_address', 'is_active', 
            'is_excluded_from_tracking', 'created_at', 
            'current_streak', 'total_earnings'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_wallet_address(self, value):
        """Validate Stacks wallet address format"""
        if not value.startswith('SP') and not value.startswith('SM'):
            raise serializers.ValidationError(
                "Invalid stacks wallet address format. Must start with 'SP' or 'SM'"
            )
        if len(value) not in [40, 41]: # Stacks address average lenght
            raise serializers.ValidationError(
                "Invalid Stacks wallet address lenght"
            )
        return value
    

class AccountListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    status = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            'id', 'email', 'wallet_address', 'current_streak', 
            'total_earnings', 'status'
        ]

    def get_status(self, obj):
        if not obj.is_active:
            return 'inactive'
        elif obj.is_excluded_from_tracking:
            return 'excluded'
        else:
            return 'active'
        

class AccountSummarySerializer(serializers.ModelSerializer):
    """Summary serializer for dashboard overview"""
    recent_submissions = serializers.SerializerMethodField()
    balance_status = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            'id', 'email', 'current_streak', 'total_earnings',
            'recent_submissions', 'balance_status'
        ]
    
    def get_recent_submissions(self, obj):
        # To be implemented
        return 0
    
    def get_balance_status(self, obj):
        # To be implemented
        return 'ok'
    

class AccountCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new accounts"""
    class Meta:
        model = Account
        fields = ['email', 'wallet_address']

    def validate_email(self, value):
        """"Ensure email is unique and valid"""
        if Account.objects.filter(email=value).exists():
            raise serializers.ValidationError("Account with this email already exist")
        return value
    

class AccountUpdateSerializer(serializers.ModelSerializer):
    """Seriallizer for updating account settings"""
    class Meta:
        model = Account
        fields = [
            'wallet_address', 'is_active', 'is_excluded_from_tracking'
        ]
        