import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

const APIURL = 'http://localhost:5002/history/recent/';

@Injectable({
  providedIn: 'root'
})
export class HistoryService {

  constructor(private http: HttpClient) {}

  getAll(): Observable<History[]> {
    return this.http.get<History[]>(APIURL);
  }
}
