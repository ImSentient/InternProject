from django.urls import path
from .views import *

urlpatterns = [
    path('servers/', ServerCreateView.as_view(), name='servers'),
    path('servers/<int:pk>/', ServerDetailView.as_view(), name='server-detail'),
    path('devices/', DeviceCreateView.as_view(), name='devices'),
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail')
]