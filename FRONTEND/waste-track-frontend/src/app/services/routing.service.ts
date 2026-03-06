import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class RoutingService {
    private apiUrl = `${environment.apiUrl}/api/routes/`;

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
