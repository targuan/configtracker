import { Component, inject  } from '@angular/core';
import {NgComponentOutlet} from '@angular/common'
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

import {  ClrVerticalNavModule, ClrModalModule } from '@clr/angular';
import { ClarityIcons, dashboardIcon, tasksIcon, networkSwitchIcon, infoCircleIcon, cloudIcon, folderIcon, timesIcon, vmBugIcon} from '@clr/angular/icon';

import { AlertService } from '../../services/alert.service';
import { ModalService } from '../../services/modal.service';

@Component({
  selector: 'app-shell',
  imports: [
    NgComponentOutlet,
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    ClrVerticalNavModule,
    ClrModalModule
  ],
  templateUrl: './shell.html',
  styleUrl: './shell.css'
})
export class Shell {

  modalOpen = false;

  protected readonly alertService = inject(AlertService);
  protected readonly modalService = inject(ModalService);

  constructor() {
    ClarityIcons.addIcons(dashboardIcon, tasksIcon, networkSwitchIcon,infoCircleIcon,cloudIcon, folderIcon, timesIcon,vmBugIcon);
  }
}