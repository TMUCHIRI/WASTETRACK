import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class RoutingService {
    private apiUrl = 'http://127.0.0.1:8000/api/routes/';

    constructor(private http: HttpClient) { }

    getRoutes(): Observable<any> {
        return this.http.get(this.apiUrl);
    }

    generateRoute(latitude: number, longitude: number): Observable<any> {
        return this.http.post(`${this.apiUrl}generate/`, { latitude, longitude });
    }

    getRoute(id: number): Observable<any> {
        return this.http.get(`${this.apiUrl}${id}/`);
    }
}
