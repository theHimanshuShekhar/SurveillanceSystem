import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

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

  getThumb(path) {
    return this.http.get('http://localhost:5000/thumb');
  }

  getVideo(path) {
    return this.http.get('http://localhost:5000/video', { params: new HttpParams().set('path', path) });
  }
}
