from django.urls import path
from .views import (
    DeviceListView, DeviceDetailView, DeviceCreateView, DeviceUpdateView, DeviceDeleteView,
    ConfigurationListView, ConfigurationDetailView, ConfigurationCreateView, ConfigurationUpdateView, ConfigurationDeleteView
)

urlpatterns = [
    path('devices/', DeviceListView.as_view(), name='device-list'),
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('devices/new/', DeviceCreateView.as_view(), name='device-create'),
    path('devices/<int:pk>/edit/', DeviceUpdateView.as_view(), name='device-update'),
    path('devices/<int:pk>/delete/', DeviceDeleteView.as_view(), name='device-delete'),
    
    path('configurations/', ConfigurationListView.as_view(), name='configuration-list'),
    path('configurations/<int:pk>/', ConfigurationDetailView.as_view(), name='configuration-detail'),
    path('configurations/new/', ConfigurationCreateView.as_view(), name='configuration-create'),
    path('configurations/<int:pk>/edit/', ConfigurationUpdateView.as_view(), name='configuration-update'),
    path('configurations/<int:pk>/delete/', ConfigurationDeleteView.as_view(), name='configuration-delete'),
]
