import { Routes } from '@angular/router';

import { Shell } from './core/layout/shell/shell';
import { Dashboard } from './pages/dashboard/dashboard';
import { Devices } from './pages/devices/devices';
import { Tasks } from './pages/tasks/tasks';

export const routes: Routes = [
  {
    path: '',
    component: Shell,
    children: [
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
      },
      {
        path: 'dashboard',
        component: Dashboard
      },
      {
        path: 'devices',
        component: Devices
      },
      {
        path: 'tasks',
        component: Tasks
      }
    ]
  }
];