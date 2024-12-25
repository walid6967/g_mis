from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'supplier', 'inventory', 'quantity', 'trans_date', 'is_deleted']
