from django.contrib.auth.models import Group, User
from .models import Transaction
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import permissions, viewsets

from .serializers import InvestmentAccountSerializer, UserSerializer, TransactionSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [DjangoModelPermissions]


class InvestmentAccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = InvestmentAccountSerializer
    permission_classes = [DjangoModelPermissions]


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited
    """
    queryset = Transaction.objects.all().order_by('created')
    permission_classes = [DjangoModelPermissions]
    serializer_class = TransactionSerializer
    """permission_classes = [DjangoModelPermissions]"""
    def get_queryset(self):
        user = self.request.user
        permissions = user.get_group_permissions()
        if 'investmentmanager.view_transaction' in permissions:
            return Transaction.objects.all().order_by('created')
        else:
            return Transaction.objects.none()
        
