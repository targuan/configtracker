import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Device {
  id: number;
  name: string;
  created: string;
  modified: string;
  device_configurations?: any[];
}

export interface DeviceCreate {
  name: string;
}

@Injectable({
  providedIn: 'root'
})
export class DeviceService {

  private readonly http = inject(HttpClient);
  private readonly apiUrl = '/api/devices';

  getAll(): Observable<Device[]> {
    return this.http.get<Device[]>(this.apiUrl);
  }

  getById(id: number): Observable<Device> {
    return this.http.get<Device>(`${this.apiUrl}/${id}`);
  }

  create(device: DeviceCreate): Observable<Device> {
    return this.http.post<Device>(this.apiUrl, device);
  }

  update(id: number, device: Partial<DeviceCreate>): Observable<Device> {
    return this.http.patch<Device>(`${this.apiUrl}/${id}`, device);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
