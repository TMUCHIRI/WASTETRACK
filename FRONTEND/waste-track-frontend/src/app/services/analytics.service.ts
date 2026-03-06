import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class AnalyticsService {
    private apiUrl = 'http://127.0.0.1:8000/api/analytics/';

    constructor(private http: HttpClient) { }

    getStats(): Observable<any> {
        return this.http.get(`${this.apiUrl}stats/`);
    }

    getLogs(): Observable<any> {
        return this.http.get(`${this.apiUrl}logs/`);
    }

    logWaste(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}logs/`, data);
    }

    getTips(): Observable<any> {
        return this.http.get(`${this.apiUrl}tips/`);
    }

    exportLogs(): void {
        this.http.get(`${this.apiUrl}logs/export/`, { responseType: 'blob' }).subscribe(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `waste_logs_${new Date().getTime()}.csv`;
            a.click();
            window.URL.revokeObjectURL(url);
        });
    }

}
