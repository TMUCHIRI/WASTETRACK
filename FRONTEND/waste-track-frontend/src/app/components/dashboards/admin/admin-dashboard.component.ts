import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatMenuModule } from '@angular/material/menu';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatSliderModule } from '@angular/material/slider';
import { GoogleMapsModule } from '@angular/google-maps';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { ReportDetailsComponent } from '../../report-details/report-details.component';

import { ReportService } from '../../../services/report.service';
import { AuthService } from '../../../services/auth.service';
import { AnalyticsService } from '../../../services/analytics.service';
import { SchedulingService } from '../../../services/scheduling.service';
import { TrackingService } from '../../../services/tracking.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
    MatButtonModule,
    MatTableModule,
    MatMenuModule,
    MatSnackBarModule,
    MatFormFieldModule,
    MatInputModule,
    MatTooltipModule,
    MatSliderModule,
    GoogleMapsModule,
    MatDialogModule
  ],



  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.css']
})
export class AdminDashboardComponent implements OnInit, OnDestroy {
  activeTab = 'stats';
  today = new Date();
  stats: any;
  reports: any[] = [];
  collectors: any[] = [];
  users: any[] = [];
  weightStats: any;
  isLoading = false;
  searchTerm = '';
  feedbackSearchTerm = '';

  // AI & Savings
  clusters: any[] = [];
  regions: any[] = [];

  get feedbackReports() {
    const term = this.feedbackSearchTerm.toLowerCase();
    return this.reports.filter(r =>
      r.collector_feedback &&
      (!term || r.waste_type?.toLowerCase().includes(term) || r.collector_feedback?.toLowerCase().includes(term))
    );
  }

  // Live Tracking Map
  mapCenter: google.maps.LatLngLiteral = { lat: -1.286389, lng: 36.817222 };
  mapZoom = 12;
  liveMarkers: any[] = [];
  private trackingSub: Subscription | null = null;

  constructor(
    private reportService: ReportService,
    private authService: AuthService,
    private analyticsService: AnalyticsService,
    private schedulingService: SchedulingService,
    private trackingService: TrackingService,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) { }

  viewReport(report: any) {
    const dialogRef = this.dialog.open(ReportDetailsComponent, {
      width: '640px',
      data: { report, role: 'admin' }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result && result.action === 'verify') {
        this.verifyReport(report.id, result.isAccurate, result.feedback);
      }
    });
  }

  openPhotoModal(imageUrl: string) {
    this.dialog.open(ReportDetailsComponent, {
      width: '600px',
      data: { report: { image: imageUrl, id: 'Preview' }, role: 'viewer' }
    });
  }

  ngOnInit() {
    this.refreshData();

    this.trackingService.connect();
    this.trackingSub = this.trackingService.locationUpdates$.subscribe(update => {
      this.updateLiveLocation(update);
    });
  }

  refreshData() {
    this.isLoading = true;
    this.loadStats();
    this.loadReports();
    this.loadWeightStats();
    this.loadUsers();
    this.loadClusters();
    this.loadRegions();
    setTimeout(() => this.isLoading = false, 800);
  }


  ngOnDestroy() {
    if (this.trackingSub) this.trackingSub.unsubscribe();
  }

  updateLiveLocation(update: any) {
    const index = this.liveMarkers.findIndex(m => m.collector_id === update.collector_id);
    const collector = this.collectors.find(c => c.id === update.collector_id);
    const label = collector ? `${collector.first_name}` : `Collector ${update.collector_id}`;

    const marker = {
      collector_id: update.collector_id,
      position: { lat: update.lat, lng: update.lng },
      label: label,
      title: label
    };

    if (index > -1) {
      this.liveMarkers[index] = marker;
    } else {
      this.liveMarkers.push(marker);
    }
  }

  loadUsers() {
    this.authService.getUsers().subscribe({
      next: (data: any[]) => {
        this.users = data;
        this.collectors = data.filter(u => u.role === 'collector');
      },
      error: () => this.showFeedback('Failed to load users', 'error')
    });
  }

  get filteredUsers() {
    if (!this.searchTerm) return this.users;
    const term = this.searchTerm.toLowerCase();
    return this.users.filter(u =>
      u.first_name?.toLowerCase().includes(term) ||
      u.last_name?.toLowerCase().includes(term) ||
      u.email?.toLowerCase().includes(term)
    );
  }

  changeRole(userId: number, newRole: string) {
    this.authService.updateUserRole(userId, newRole).subscribe({
      next: () => {
        this.loadUsers();
        this.showFeedback(`User promoted to ${newRole}`, 'success');
      },
      error: () => this.showFeedback('Role update failed', 'error')
    });
  }

  loadStats() {
    this.reportService.getAdminStats().subscribe((data: any) => this.stats = data);
  }

  loadReports() {
    this.reportService.getAllReports().subscribe((data: any[]) => this.reports = data);
  }

  loadWeightStats() {
    this.analyticsService.getStats().subscribe((data: any) => this.weightStats = data);
  }

  assignReport(reportId: number, collectorId: number) {
    this.reportService.assignReport(reportId, collectorId).subscribe({
      next: () => {
        this.loadReports();
        this.loadStats();
        this.showFeedback('Collector assigned successfully', 'success');
      },
      error: () => this.showFeedback('Assignment failed', 'error')
    });
  }

  private showFeedback(message: string, type: 'success' | 'error') {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      panelClass: type === 'success' ? ['success-snackbar'] : ['error-snackbar']
    });
  }

  exportLogs() {
    this.analyticsService.exportLogs();
    this.showFeedback('Preparing export...', 'success');
  }

  loadClusters() {
    this.reportService.getClusters().subscribe(data => this.clusters = data);
  }

  loadRegions() {
    this.reportService.getRegions().subscribe(data => this.regions = data);
  }

  updateThreshold(region: any, threshold: number) {
    const data = { ...region, threshold };
    this.reportService.updateRegion(data).subscribe({
      next: () => {
        this.showFeedback(`Threshold for ${region.name} updated.`, 'success');
        this.loadRegions();
      },
      error: () => this.showFeedback('Failed to update threshold', 'error')
    });
  }

  verifyReport(reportId: number, isAccurate: boolean, feedback: string = '') {
    if (!isAccurate && !feedback) {
      feedback = prompt('Please provide feedback/reason for rejection:', '') || '';
      if (feedback === null) return; // Cancelled
    }

    this.reportService.verifyReport(reportId, isAccurate, feedback).subscribe({
      next: (res) => {
        this.showFeedback(res.message, 'success');
        this.loadReports();
        this.loadStats();
      },
      error: () => this.showFeedback('Verification failed', 'error')
    });
  }

  adjustPoints(report: any, isAward: boolean) {
    if (report.points_adjusted) {
      this.showFeedback('Points for this report have already been adjusted.', 'error');
      return;
    }
    const points = isAward ? 10 : -5;
    const reason = isAward
      ? 'Collector feedback verified – bonus awarded'
      : 'Collector flagged discrepancy – points deducted';

    this.reportService.adjustUserPoints(report.user, points, reason, report.id).subscribe({
      next: () => {
        // Immediately mark the local report object so the buttons disappear
        report.points_adjusted = true;
        this.showFeedback(
          `${isAward ? '+10' : '-5'} points ${isAward ? 'awarded to' : 'deducted from'} citizen.`,
          'success'
        );
      },
      error: (err) => {
        const msg = err?.error?.error || 'Failed to adjust points';
        this.showFeedback(msg, 'error');
      }
    });
  }

  logout() {
    this.authService.logout();
  }
}

