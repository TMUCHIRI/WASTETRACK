import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ReportService {
  private apiUrl = 'http://127.0.0.1:8000/api/reports/';

  constructor(private http: HttpClient) { }

  createReport(formData: FormData): Observable<any> {
    return this.http.post(this.apiUrl, formData);
  }

  getMyReports(): Observable<any> {
    return this.http.get(`${this.apiUrl}`);
  }

  getAllReports(): Observable<any> {
    return this.http.get(`${this.apiUrl}`); // Backend handles filtering based on user role in some views, but for Admin we might need a specific view or just rely on permissions.
  }

  getAdminStats(): Observable<any> {
    return this.http.get(`${this.apiUrl}admin/stats/`);
  }

  assignReport(id: number, collectorId: number): Observable<any> {
    return this.http.patch(`${this.apiUrl}${id}/assign/`, { collector: collectorId });
  }

  updateStatus(id: number, status: string, feedback?: string, image?: File): Observable<any> {
    const formData = new FormData();
    formData.append('status', status);
    if (feedback) formData.append('collector_feedback', feedback);
    if (image) formData.append('collector_image', image);

    return this.http.patch(`${this.apiUrl}${id}/status/`, formData);
  }

  getPoints(): Observable<any> {
    return this.http.get(`${this.apiUrl}points/`);
  }

  redeemPoints(perk: string): Observable<any> {
    return this.http.post(`${this.apiUrl}points/redeem/`, { perk });
  }

  updateReport(id: number, data: any): Observable<any> {
    return this.http.patch(`${this.apiUrl}${id}/`, data);
  }

  updateReportFullness(id: number, fullness: number): Observable<any> {
    return this.updateReport(id, { estimated_fullness: fullness });
  }


  getClusters(): Observable<any> {
    return this.http.get(`${this.apiUrl}admin/clusters/`);
  }

  getRegions(): Observable<any> {
    return this.http.get(`${this.apiUrl}admin/regions/`);
  }

  updateRegion(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}admin/regions/`, data);
  }

  verifyReport(id: number, isAccurate: boolean, feedback: string = ''): Observable<any> {
    return this.http.post(`${this.apiUrl}${id}/verify/`, { is_accurate: isAccurate, feedback: feedback });
  }

  adjustUserPoints(userId: number, delta: number, reason: string = '', reportId?: number): Observable<any> {
    const body: any = { user_id: userId, delta, reason };
    if (reportId !== undefined) body.report_id = reportId;
    return this.http.post(`${this.apiUrl}admin/adjust-points/`, body);
  }

  getReport(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}${id}/`);
  }

}

