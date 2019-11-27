import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ResultService {

  constructor(private http: HttpClient) {
  }

  getResults() {
    return this.http.get('http://localhost:5000/folders');
  }

  isAlive() {
    return this.http.get('http://localhost:5000/test');
  }
}
