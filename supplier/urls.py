from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('<int:pk>', views.supplier_detail, name='supplier_detail'),
    path('create/', views.supplier_create, name='supplier_create'),
    path('update/<int:pk>', views.supplier_update, name='supplier_update'),
    path('delete/<int:pk>', views.supplier_delete, name='supplier_delete'),
]
