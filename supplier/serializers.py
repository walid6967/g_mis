from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'account','name', 'contact_person', 'email', 'phone', 'address', 'created_at', 'updated_at']
