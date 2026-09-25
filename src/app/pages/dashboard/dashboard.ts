import { Component } from '@angular/core';
import { ClrIconModule } from '@clr/angular';

@Component({
  selector: 'app-dashboard',
  imports: [
    ClrIconModule
  ],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard {}