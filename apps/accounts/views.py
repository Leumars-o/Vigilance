from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Account
from .serializers import (
    AccountSerializer, AccountListSerializer, AccountSummarySerializer,
    AccountCreateSerializer, AccountUpdateSerializer
)

class AccountViewSet(viewsets.ModelViewSet):
    """ViewSet for managing accounts

    Args:
        viewsets (_type_):
    """

    queryset = Account.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return AccountListSerializer
        elif self.action == 'create':
            return AccountCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AccountUpdateSerializer
        elif self.action == 'summary':
            return AccountSummarySerializer
        return AccountSerializer
    
    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = Account.objects.all()

        # Filter by active status
        is_active = self.request.query_params.get('active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        # Filter by tracking status
        excluded = self.request.query_params.get('excluded')
        if excluded is not None:
            queryset = queryset.filter(is_excluded_from_tracking=excluded.lower() == 'true')

        # Filter by minimum streak
        min_streak = self.request.query_params.get('min_streak')
        if min_streak:
            queryset = queryset.filter(current_streak_gte=int(min_streak))

        return queryset.order_by('-created_at')
    
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics for all accounts"""
        accounts = self.get_queryset()
        total_accounts = accounts.count()
        active_accounts = accounts.filter(is_active=True).count()
        total_earnings = accounts.aggregate(Sum('total_earnings'))['total_earnings__sum'] or 0
        
        return Response({
            'total_accounts': total_accounts,
            'active_accounts': active_accounts,
            'inactive_accounts': total_accounts - active_accounts,
            'total_earnings_across_all': total_earnings,
            'average_earnings': total_earnings / total_accounts if total_accounts > 0 else 0
        })
    

    @action(detail=True, methods=['post'])
    def toggle_tracking(self, request, pk=None):
        """Toggle tracking status for an account"""
        account = self.get_object()
        account.is_excluded_from_tracking = not account.is_excluded_from_tracking
        account.save()

        serializer = self.get_serializer(account)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_tracking(self, request, pk=None):
        """Toggle tracking status for an account"""
        account = self.get_object()
        account.is_excluded_from_tracking = not account.is_excluded_from_tracking
        account.save()
        
        serializer = self.get_serializer(account)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reset_streak(self, request, pk=None):
        """Reset streak for an account"""
        account = self.get_object()
        account.current_streak = 0
        account.save()
        
        return Response({
            'message': f'Streak reset for {account.email}',
            'current_streak': account.current_streak
        })