import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class SchedulingService {
    private apiUrl = `${environment.apiUrl}/api/scheduling/`;

    constructor(private http: HttpClient) { }

    getRegions(): Observable<any> {
        return this.http.get(`${this.apiUrl}regions/`);
    }

    createRegion(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}regions/`, data);
    }

    getTeams(): Observable<any> {
        return this.http.get(`${this.apiUrl}teams/`);
    }

    createTeam(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}teams/`, data);
    }

    getSchedules(): Observable<any> {
        return this.http.get(`${this.apiUrl}schedules/`);
    }

    createSchedule(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}schedules/`, data);
    }

    getScheduleDetails(id: number): Observable<any> {
        return this.http.get(`${this.apiUrl}schedules/${id}/`);
    }
}
