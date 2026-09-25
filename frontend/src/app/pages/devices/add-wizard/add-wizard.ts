import { Component, ViewChild } from '@angular/core';
import { ClrWizard, ClrWizardModule } from '@clr/angular';

@Component({
  selector: 'app-add-wizard',
  imports: [ClrWizardModule],
  templateUrl: './add-wizard.html',
  styleUrl: './add-wizard.css',
})
export class AddWizard {
  @ViewChild('wizard', { static: true }) public wizard: ClrWizard | undefined;
  wizardOpen = false;
}
