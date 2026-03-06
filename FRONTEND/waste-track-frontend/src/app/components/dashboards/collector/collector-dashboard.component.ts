import { Component, OnInit, OnDestroy } from '@angular/core';

import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatTooltipModule } from '@angular/material/tooltip';
import { GoogleMapsModule } from '@angular/google-maps';
import { ReportService } from '../../../services/report.service';
import { AuthService } from '../../../services/auth.service';
import { SchedulingService } from '../../../services/scheduling.service';
import { RoutingService } from '../../../services/routing.service';
import { AnalyticsService } from '../../../services/analytics.service';
import { TrackingService } from '../../../services/tracking.service';

import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { ReportDetailsComponent } from '../../report-details/report-details.component';

@Component({

  selector: 'app-collector-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
    MatButtonModule,
    MatTableModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    MatTooltipModule,
    GoogleMapsModule,
    MatSnackBarModule,
    MatDialogModule
  ],
  templateUrl: './collector-dashboard.component.html',
  styleUrls: ['./collector-dashboard.component.css']
})
export class CollectorDashboardComponent implements OnInit, OnDestroy {
  activeTab = 'schedules';
  collectorName = '';

  schedules: any[] = [];
  pendingSchedules: any[] = [];
  historySchedules: any[] = [];
  optimizedRoute: any = null;
  private trackInterval: any;

  // Map Config
  center: google.maps.LatLngLiteral = { lat: -1.286389, lng: 36.817222 };
  zoom = 12;
  routeMarkers: any[] = [];

  constructor(
    private reportService: ReportService,
    private authService: AuthService,
    private schedulingService: SchedulingService,
    private routingService: RoutingService,
    private analyticsService: AnalyticsService,
    private trackingService: TrackingService,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) { }

  viewReport(report: any) {
    const dialogRef = this.dialog.open(ReportDetailsComponent, {
      width: '600px',
      data: { report, role: 'collector' }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result && result.action === 'collected') {
        this.reportService.updateStatus(report.id, 'collected', result.feedback, result.image).subscribe({
          next: () => {
            this.snackBar.open('Collection verified and status updated!', 'Close', { duration: 3000 });
            this.loadSchedules();
          },
          error: () => this.snackBar.open('Failed to update status', 'Close', { duration: 3000 })
        });
      }
    });
  }

  ngOnInit() {
    this.authService.currentUser$.subscribe(user => {
      if (user) {
        this.collectorName = `${user.first_name} ${user.last_name}`;
        this.loadSchedules();
        this.getCurrentLocation();
        this.trackingService.connect();

        // Start tracking with real user id
        if (this.trackInterval) clearInterval(this.trackInterval);
        this.trackInterval = setInterval(() => {
          this.getCurrentLocation();
          this.trackingService.sendLocation(user.id, this.center.lat, this.center.lng);
        }, 10000);
      }
    });
  }


  ngOnDestroy() {
    if (this.trackInterval) clearInterval(this.trackInterval);
  }


  loadSchedules() {
    this.schedulingService.getSchedules().subscribe((data: any[]) => {
      this.schedules = data;
      this.pendingSchedules = data.filter(s => s.report_details.status !== 'collected');
      this.historySchedules = data.filter(s => s.report_details.status === 'collected');
    });
  }


  getCurrentLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        this.center = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
      });
    }
  }

  generateRoute() {
    this.routingService.generateRoute(this.center.lat, this.center.lng).subscribe((data: any) => {
      this.optimizedRoute = data;
      this.updateMapMarkers();
    });
  }

  updateMapMarkers() {
    this.routeMarkers = this.optimizedRoute.route_data.map((step: any) => ({
      position: { lat: step.latitude, lng: step.longitude },
      title: `${step.waste_type} (${step.urgency})`
    }));
  }

  updateStatus(reportId: number, status: string) {
    this.reportService.updateStatus(reportId, status).subscribe(() => {
      this.loadSchedules();
    });
  }

  logWaste(data: any) {
    this.analyticsService.logWaste(data).subscribe(() => {
      this.snackBar.open('Waste weight logged successfully!', 'Close', { duration: 3000 });
    });
  }

  logout() {
    this.authService.logout();
  }
}
