from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = [('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')]
    created = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    description = models.TextField(default='')
    transactiontype = models.CharField(max_length=100, choices=TRANSACTION_TYPES, default='deposit')
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)


    class Meta:
        ordering = ['created']
    def __str__(self):
        # Return the title of the transaction
        return f"{self.user.username}"
