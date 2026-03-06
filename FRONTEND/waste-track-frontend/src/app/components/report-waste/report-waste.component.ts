import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { RouterModule } from '@angular/router';
import { GoogleMapsModule } from '@angular/google-maps';
import { AuthService } from '../../services/auth.service';
import { ReportService } from '../../services/report.service';

import { MatSliderModule } from '@angular/material/slider';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

@Component({
  selector: 'app-report-waste',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatIconModule,
    MatButtonModule,
    GoogleMapsModule,
    RouterModule,
    MatSnackBarModule,
    MatSliderModule,
  ],
  templateUrl: './report-waste.component.html',
  styleUrls: ['./report-waste.component.css']
})
export class ReportWasteComponent implements OnInit {
  report = {
    waste_type: 'general',
    urgency: 'medium',
    description: '',
    latitude: 0,
    longitude: 0,
    estimated_fullness: 100
  };

  isEditMode = false;
  editReportId: number | null = null;

  imageFile: File | null = null;
  imagePreview: string | null = null;
  isSubmitting = false;
  gettingLocation = false;

  // Google Maps
  googleMapsLoaded = false;
  mapCenter = { lat: -1.2921, lng: 36.8219 }; // Nairobi
  // Map Config
  center: google.maps.LatLngLiteral = { lat: -1.286389, lng: 36.817222 };
  zoom = 12;
  markerPosition: google.maps.LatLngLiteral | null = null;

  constructor(
    private reportService: ReportService,
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    this.loadGoogleMaps();
  }

  ngOnInit(): void {
    const navigation = this.router.getCurrentNavigation();
    const editData = navigation?.extras?.state?.['report'];

    if (editData) {
      this.isEditMode = true;
      this.editReportId = editData.id;
      this.report = {
        waste_type: editData.waste_type,
        urgency: editData.urgency || 'medium',
        description: editData.description || '',
        latitude: editData.latitude,
        longitude: editData.longitude,
        estimated_fullness: editData.estimated_fullness
      };
      this.markerPosition = { lat: editData.latitude, lng: editData.longitude };
      this.mapCenter = { lat: editData.latitude, lng: editData.longitude };
      this.imagePreview = editData.image;
    }
  }

  loadGoogleMaps() {
    if ((window as any).google?.maps) {
      this.googleMapsLoaded = true;
    } else {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyDUxdr3rsPga1iDZ1DBUibwz5o_oM1f7qU`;
      script.onload = () => this.googleMapsLoaded = true;
      document.body.appendChild(script);
    }
  }

  onMapClick(event: any) {
    if (event?.latLng) {
      const lat = event.latLng.lat();
      const lng = event.latLng.lng();
      this.report.latitude = lat;
      this.report.longitude = lng;
      this.markerPosition = { lat, lng };
    }
  }

  onFileSelect(event: any) {
    const file = event.target?.files?.[0];
    if (file) {
      this.imageFile = file;
      const reader = new FileReader();
      reader.onload = (e: any) => (this.imagePreview = e.target.result);
      reader.readAsDataURL(file);
    }
  }

  getLocation() {
    if (!navigator.geolocation) {
      this.snackBar.open('Geolocation not supported', 'Close', { duration: 3000 });
      return;
    }

    this.gettingLocation = true;
    navigator.geolocation.getCurrentPosition(
      (position) => {
        this.report.latitude = position.coords.latitude;
        this.report.longitude = position.coords.longitude;
        this.markerPosition = { lat: this.report.latitude, lng: this.report.longitude };
        this.gettingLocation = false;
      },
      () => {
        this.snackBar.open('Unable to get location. Please enable GPS.', 'Close', { duration: 3000 });
        this.gettingLocation = false;
      }
    );
  }

  logout() {
    this.authService.logout();
  }

  onSubmit() {
    if (!this.imageFile || !this.report.latitude) {
      this.snackBar.open('Please add a photo and select a location on the map.', 'Close', { duration: 3000 });
      return;
    }

    this.isSubmitting = true;

    if (this.isEditMode && this.editReportId) {
      const updateData: any = {
        waste_type: this.report.waste_type,
        description: this.report.description,
        urgency: this.report.urgency,
        estimated_fullness: this.report.estimated_fullness
      };
      // Note: We don't usually update location or image in a simple edit, but we could.
      // For resubmission, user might want to update image.

      this.reportService.updateReport(this.editReportId, updateData).subscribe({
        next: (res) => {
          this.snackBar.open(res.message || 'Report updated successfully!', 'Close', { duration: 4000 });
          this.router.navigate(['/dashboard']);
        },

        error: err => {
          this.snackBar.open('Error: ' + err.message, 'Close', { duration: 5000 });
          this.isSubmitting = false;
        }
      });
      return;
    }

    const fd = new FormData();
    fd.append('image', this.imageFile);
    fd.append('waste_type', this.report.waste_type);
    fd.append('description', this.report.description);
    fd.append('urgency', this.report.urgency);
    fd.append('latitude', this.report.latitude.toString());
    fd.append('longitude', this.report.longitude.toString());
    fd.append('estimated_fullness', this.report.estimated_fullness.toString());

    this.reportService.createReport(fd).subscribe({
      next: (res) => {
        if (res.warning) {
          this.snackBar.open('Success: ' + res.warning, 'Got it', { duration: 6000 });
        } else {
          this.snackBar.open('Waste reported successfully!', 'Close', { duration: 3000 });
        }
        this.router.navigate(['/dashboard']);
      },

      error: err => {
        this.snackBar.open('Error: ' + err.message, 'Close', { duration: 5000, panelClass: ['error-snackbar'] });
        this.isSubmitting = false;
      }
    });
  }
}
