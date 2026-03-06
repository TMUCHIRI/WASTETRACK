import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { GoogleMapsModule } from '@angular/google-maps';
import { RouterModule } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { AuthService } from '../../services/auth.service';
import { ReportService } from '../../services/report.service';

import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatSliderModule } from '@angular/material/slider';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    GoogleMapsModule,
    RouterModule,
    MatIconModule,
    MatSnackBarModule,
    MatSliderModule,
    MatButtonModule,
    MatTooltipModule
  ],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  reports: any[] = [];
  points: number = 0;
  googleMapsLoaded = false;
  mapCenter = { lat: -1.2921, lng: 36.8219 };

  constructor(
    private reportService: ReportService,
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit() {
    this.loadGoogleMaps();
    this.loadReports();
    this.loadPoints();
  }

  loadPoints() {
    this.reportService.getPoints().subscribe({
      next: (res) => this.points = res.points,
      error: () => console.error('Failed to load points')
    });
  }

  redeem(perk: string) {
    this.reportService.redeemPoints(perk).subscribe({
      next: (res) => {
        this.snackBar.open(res.message, 'Close', { duration: 3000 });
        this.loadPoints();
      },
      error: (err) => this.snackBar.open(err.error?.message || 'Redemption failed', 'Close', { duration: 3000 })
    });
  }


  loadGoogleMaps() {
    if ((window as any).google?.maps) {
      this.googleMapsLoaded = true;
    } else {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyDUxdr3rsPga1iDZ1DBUibwz5o_oM1f7qU`;
      script.onload = () => {
        this.googleMapsLoaded = true;
        if (this.reports.length > 0) {
          this.mapCenter = { lat: this.reports[0].latitude, lng: this.reports[0].longitude };
        }
      };
      document.body.appendChild(script);
    }
  }

  loadReports() {
    this.reportService.getMyReports().subscribe({
      next: (data) => {
        this.reports = data;
        if (this.googleMapsLoaded && data.length > 0) {
          this.mapCenter = { lat: data[0].latitude, lng: data[0].longitude };
        }
      },
      error: () => this.snackBar.open('Failed to load reports', 'Close', { duration: 3000 })
    });
  }

  updateFullness(report: any, newFullness: number) {
    if (report.estimated_fullness === newFullness) return;
    this.reportService.updateReportFullness(report.id, newFullness).subscribe({
      next: (res) => {
        const msg = res.message || 'Report updated successfully!';
        this.snackBar.open(msg, 'Close', { duration: 4000 });
        this.loadReports();
        this.loadPoints();
      },
      error: () => this.snackBar.open('Update failed', 'Close', { duration: 3000 })
    });
  }

  editReport(report: any) {
    this.router.navigate(['/report'], { state: { report } });
  }


  getMarkerOptions(report: any) {
    const color = report.urgency === 'high' ? '#d32f2f' :
      report.urgency === 'medium' ? '#f57c00' : '#388e3c';
    const symbolPath = (window as any).google?.maps?.SymbolPath?.CIRCLE;
    return {
      icon: {
        path: symbolPath ?? undefined,
        fillColor: color,
        fillOpacity: 0.9,
        strokeWeight: 2,
        strokeColor: '#fff',
        scale: 10
      }
    };
  }

  logout() {
    this.authService.logout();
  }
}
