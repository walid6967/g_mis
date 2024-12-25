from django.db import models
from supplier.models import Supplier
from inventory.models import Inventory


class Transaction(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    trans_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False) 
    def __str__(self):
        return f"Create transaction {self.pk} - for: {self.supplier}"