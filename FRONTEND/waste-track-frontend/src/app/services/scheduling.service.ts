import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class SchedulingService {
    private apiUrl = 'http://127.0.0.1:8000/api/scheduling/';

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
