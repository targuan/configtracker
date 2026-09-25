import { Injectable, signal } from '@angular/core';

export type AlertType =
  | 'info'
  | 'success'
  | 'warning'
  | 'danger';

export interface AppAlert {
  type: AlertType;
  message: string;
  actionLabel?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AlertService {

  readonly alert = signal<AppAlert | null>(null);

  show(
    type: AlertType,
    message: string,
    actionLabel?: string
  ): void {
    this.alert.set({
      type,
      message,
      actionLabel
    });
  }

  info(message: string, actionLabel?: string): void {
    this.show('info', message, actionLabel);
  }

  success(message: string, actionLabel?: string): void {
    this.show('success', message, actionLabel);
  }

  warning(message: string, actionLabel?: string): void {
    this.show('warning', message, actionLabel);
  }

  danger(message: string, actionLabel?: string): void {
    this.show('danger', message, actionLabel);
  }

  close(): void {
    this.alert.set(null);
  }
}