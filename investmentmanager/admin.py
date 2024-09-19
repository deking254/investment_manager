from django.contrib import admin
from .models import Transaction
#admin.site.register(Transaction)
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transactiontype', 'created', 'balance')
    list_filter = ('user', ('created', admin.DateFieldListFilter))
    ordering = ("created",)

# Register your models here.
