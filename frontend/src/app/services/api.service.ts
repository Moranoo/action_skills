import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://127.0.0.1:5000/evenements';  // URL de ton API backend

  constructor(private http: HttpClient) { }

  // Méthode pour récupérer les événements
  getEvents(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }
}
