import { Component, inject, ViewChild, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ClrDatagridModule, ClrDatagridStringFilterInterface } from '@clr/angular';
import { AlertService } from '../../core/services/alert.service';
import { ModalService } from '../../core/services/modal.service';
import { DeviceService, Device } from '../../core/services/device.service';
import { AddWizard } from './add-wizard/add-wizard';

@Component({
  selector: 'app-devices',
  imports: [CommonModule, FormsModule, ClrDatagridModule, AddWizard],
  templateUrl: './devices.html',
  styleUrl: './devices.css'
})
export class Devices implements OnInit {
  @ViewChild('wizard', { static: true }) wizard: AddWizard | undefined;

  devices = signal<Device[]>([]);
  loading = signal<boolean>(false);
  selectedDevices: Device[] = [];

  private readonly alertService = inject(AlertService);
  private readonly modalService = inject(ModalService);
  private readonly deviceService = inject(DeviceService);

  ngOnInit(): void {
    this.loadDevices();
  }

  loadDevices(): void {
    this.loading.set(true);
    this.deviceService.getAll().subscribe({
      next: (devices) => {
        this.devices.set(devices);
        this.loading.set(false);
      },
      error: (err) => {
        this.alertService.danger('Failed to load devices');
        this.loading.set(false);
      }
    });
  }

  openWizard() {
    this.wizard?.wizard?.reset();
    this.wizard?.wizard?.open();
  }

  save(): void {
    this.alertService.success(
      'The device has been successfully saved.'
    );
  }

  add(): void {
    this.openWizard();
  }

  deleteSelected(): void {
    if (this.selectedDevices.length === 0) {
      this.alertService.warning('Please select at least one device to delete');
      return;
    }

    if (confirm('Are you sure you want to delete the selected devices?')) {
      this.selectedDevices.forEach(device => {
        this.deviceService.delete(device.id).subscribe({
          next: () => {
            this.loadDevices();
            this.selectedDevices = [];
            this.alertService.success('Devices deleted successfully');
          },
          error: (err) => {
            this.alertService.danger('Failed to delete device');
          }
        });
      });
    }
  }

  deleteDevice(device: Device): void {
    if (confirm(`Are you sure you want to delete ${device.name}?`)) {
      this.deviceService.delete(device.id).subscribe({
        next: () => {
          this.loadDevices();
          this.alertService.success('Device deleted successfully');
        },
        error: (err) => {
          this.alertService.danger('Failed to delete device');
        }
      });
    }
  }

  onDeviceCreated(device: Device): void {
    this.loadDevices();
    this.alertService.success('Device created successfully');
  }
}