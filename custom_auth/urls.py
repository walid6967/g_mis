from django.urls import path
from .views import get_access_token

urlpatterns = [
    path('get_token/', get_access_token, name='get_access_token'),
]
