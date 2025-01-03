from django.db import models
from account.models import Account

class Supplier(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='suppliers') 
    name = models.CharField(max_length=255) 
    contact_person = models.CharField(max_length=255, blank=True, null=True)  
    email = models.EmailField(unique=True, blank=True, null=True) 
    phone = models.CharField(max_length=15, blank=True, null=True)  
    address = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    is_deleted = models.BooleanField(default=False) 

    def __str__(self):
        return self.name
