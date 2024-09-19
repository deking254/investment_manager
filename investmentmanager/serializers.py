from django.contrib.auth.models import Group, User
from .models import Transaction
from rest_framework import serializers
from django.db.models import Sum


class UserSerializer(serializers.HyperlinkedModelSerializer):
    transactions = serializers.HyperlinkedRelatedField(many=True, view_name='transaction-detail', read_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'password', 'transactions']


class InvestmentAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', queryset=User.objects.all())
    transactiontype = serializers.ChoiceField(choices=Transaction.TRANSACTION_TYPES)
    class Meta:
        model = Transaction
        fields = ['url', 'transactiontype', 'amount', 'description', 'user']
    def create(self, validated_data):
        # Access the user from the context
        request = self.context.get('request')
        user = request.user if request else None
        
        # Ensure the user is authenticated
        if user and user.is_authenticated:
            validated_data['user'] = user
        
        # Call the parent create method
        return super().create(validated_data)
    def validate(self, data):
        transactiontype = data.get('transactiontype')
        amount = data.get('amount')
        selected_user_transactions = Transaction.objects.filter(user=data['user']);
        data['balance'] = selected_user_transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        # Modify amount based on status
        if transactiontype == 'deposit':
            # Ensure amount is positive for completed transactions
            if amount < 0:
                data['amount'] = abs(amount)
            data['balance'] += data['amount']
        elif transactiontype == 'withdrawal':
            # Ensure amount is negative for failed transactions
            if amount > 0:
                data['amount'] = -amount
            data['balance'] += data['amount']
        # For 'pending', the amount remains unchanged
        return data
