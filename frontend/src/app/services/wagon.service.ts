import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Wagon} from '../models/wagon';

const APIURL = 'http://localhost:5002/wagon/';

@Injectable({
  providedIn: 'root'
})

export class WagonService {
  constructor(private http: HttpClient) {}

  getAll(): Observable<Wagon[]> {
    return this.http.get<Wagon[]>(APIURL);
  }

  getById(id: number): Observable<Wagon> {
    return this.http.get<Wagon>(APIURL + id);
  }

  addWagon(id: number, longitude: number, latitude: number): Observable<Wagon> {
    return this.http.get<Wagon>(APIURL + id + '/pin/lat/' + latitude + '/long/' + longitude);
  }

  deleteWagon(id: number): Observable<Wagon> {
    return this.http.get<Wagon>(APIURL + 'delete/' + id);
  }

  addExpectedWagon(wagon_id: number): Observable<Wagon> {
    return this.http.get<Wagon>(APIURL + 'new/' + wagon_id);
  }
}
