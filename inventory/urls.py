from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventories, name='inventories'),
    path('<int:id>', views.get_inventory, name='get_inventory'),
    path('create/', views.create_inventory, name='create_inventory'),
    path('update/<int:id>', views.update_inventory, name='update_inventory'),
    path('delete/<int:id>', views.delete_inventory, name='delete_inventory'),
]
