import { Component, inject, ViewChild } from '@angular/core';
import { AlertService } from '../../core/services/alert.service';
import { ModalService } from '../../core/services/modal.service';
import { AddWizard } from './add-wizard/add-wizard';

@Component({
  selector: 'app-devices',
  imports: [AddWizard],
  templateUrl: './devices.html',
  styleUrl: './devices.css'
})
export class Devices {
  @ViewChild('wizard', { static: true }) wizard: AddWizard | undefined;

  

  private readonly alertService = inject(AlertService);
  private readonly modalService = inject(ModalService);

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
    this.openWizard()
  //   this.modalService.open({
  //     title: 'Add device',
  //     component: AddWizard,
  //     size: 'lg'
  //   });
  }
}