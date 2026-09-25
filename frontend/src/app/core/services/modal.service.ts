import { Injectable, Type, signal } from '@angular/core';

export interface ModalConfig {
  title: string;
  component: Type<unknown>;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

@Injectable({
  providedIn: 'root'
})
export class ModalService {

  readonly modal = signal<ModalConfig | null>(null);

  open(config: ModalConfig): void {
    this.modal.set(config);
  }

  close(): void {
    this.modal.set(null);
  }
}