from django.urls import path
from . import views

urlpatterns = [
    path('', views.transactions, name='transactions'),
    path('<int:id>', views.get_transaction, name='get_transaction'),
    path('create/', views.create_transaction, name='create_transaction'),
    path('update/<int:id>', views.update_transaction, name='update_transaction'),
    path('delete/<int:id>', views.delete_transaction, name='delete_transaction'),
]
