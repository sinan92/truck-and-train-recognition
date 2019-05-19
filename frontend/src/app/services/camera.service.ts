import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Camera} from '../models/camera';
import {Observable} from 'rxjs';

const APIURL = 'http://localhost:5002/camera/';

@Injectable({
  providedIn: 'root'
})
export class CameraService {
  constructor(private http: HttpClient) {}

  getAll(): Observable<Camera[]> {
    return this.http.get<Camera[]>(APIURL + 'with/wagons');
  }

  getById(camera_id: number): Observable<Camera> {
    return this.http.get<Camera>(APIURL + camera_id);
  }

  saveCamera(camera_id: number, description: string): Observable<Camera> {
    return this.http.get<Camera>(APIURL + camera_id + '/description/' + description);
  }
}
