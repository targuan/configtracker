import { Component, ViewChild, inject, output, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ClrWizard, ClrWizardModule, ClrInputModule, ClrButtonModule } from '@clr/angular';
import { DeviceService, Device } from '../../../core/services/device.service';

@Component({
  selector: 'app-add-wizard',
  imports: [CommonModule, FormsModule, ClrWizardModule, ClrInputModule, ClrButtonModule],
  templateUrl: './add-wizard.html',
  styleUrl: './add-wizard.css',
})
export class AddWizard {
  @ViewChild('wizard', { static: true }) public wizard: ClrWizard | undefined;
  wizardOpen = false;

  deviceName = signal<string>('');
  isSubmitting = signal<boolean>(false);

  deviceCreated = output<Device>();

  private readonly deviceService = inject(DeviceService);

  open(): void {
    this.wizardOpen = true;
  }

  reset(): void {
    this.deviceName.set('');
    this.isSubmitting.set(false);
  }

  onSubmit(): void {
    if (!this.deviceName() || this.deviceName().trim() === '') {
      return;
    }

    this.isSubmitting.set(true);
    this.deviceService.create({ name: this.deviceName() }).subscribe({
      next: (device) => {
        this.deviceCreated.emit(device);
        this.reset();
        this.wizardOpen = false;
        this.isSubmitting.set(false);
      },
      error: (err) => {
        this.isSubmitting.set(false);
      }
    });
  }

  onCancel(): void {
    this.reset();
    this.wizardOpen = false;
  }
}
