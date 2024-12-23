from django.db import models

class Account(models.Model):
    title = models.CharField(max_length=255, unique=True) 
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) 
    is_deleted = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title
