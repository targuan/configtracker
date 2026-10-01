from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Device, Configuration


class DeviceListView(ListView):
    model = Device
    template_name = 'inventory/device_list.html'
    context_object_name = 'devices'


class DeviceDetailView(DetailView):
    model = Device
    template_name = 'inventory/device_detail.html'
    context_object_name = 'device'


class DeviceCreateView(CreateView):
    model = Device
    template_name = 'inventory/device_form.html'
    fields = ['name']
    success_url = reverse_lazy('device-list')


class DeviceUpdateView(UpdateView):
    model = Device
    template_name = 'inventory/device_form.html'
    fields = ['name']
    success_url = reverse_lazy('device-list')


class DeviceDeleteView(DeleteView):
    model = Device
    template_name = 'inventory/device_confirm_delete.html'
    success_url = reverse_lazy('device-list')


class ConfigurationListView(ListView):
    model = Configuration
    template_name = 'inventory/configuration_list.html'
    context_object_name = 'configurations'


class ConfigurationDetailView(DetailView):
    model = Configuration
    template_name = 'inventory/configuration_detail.html'
    context_object_name = 'configuration'


class ConfigurationCreateView(CreateView):
    model = Configuration
    template_name = 'inventory/configuration_form.html'
    fields = ['configuration']
    success_url = reverse_lazy('configuration-list')


class ConfigurationUpdateView(UpdateView):
    model = Configuration
    template_name = 'inventory/configuration_form.html'
    fields = ['configuration']
    success_url = reverse_lazy('configuration-list')


class ConfigurationDeleteView(DeleteView):
    model = Configuration
    template_name = 'inventory/configuration_confirm_delete.html'
    success_url = reverse_lazy('configuration-list')
