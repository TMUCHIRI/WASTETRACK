import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialogModule, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-report-details',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatDialogModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule
  ],
  template: `
    <h2 mat-dialog-title>Report Details #{{data.report.id}}</h2>
    <mat-dialog-content class="mat-typography">
      <div class="report-info" style="min-width: 400px; max-width: 600px;">
        <div class="photo-section" style="margin-bottom: 20px;">
          <h3 style="margin-bottom: 10px;">Citizen Photo</h3>
          <img [src]="data.report.image" alt="Waste photo" class="main-photo" (click)="zoomPhoto = !zoomPhoto" [class.zoomed]="zoomPhoto">
          <p class="hint">Click photo to toggle zoom</p>
        </div>

        <div class="details-section" style="background: f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
          <p><strong>Type:</strong> {{data.report.waste_type | titlecase}}</p>
          <p><strong>Status:</strong> <span class="badge" [class]="data.report.status">{{data.report.status}}</span></p>
          <p><strong>Description:</strong> {{data.report.description}}</p>
          <p><strong>Fullness:</strong> {{data.report.estimated_fullness}}%</p>
        </div>

        <hr style="margin: 20px 0;">

        <!-- Collector Input Section -->
        <div *ngIf="data.role === 'collector' && data.report.status === 'assigned'" class="feedback-section">
          <h3 style="color: #3f51b5;">Collection Verification</h3>
          <p style="font-size: 0.9em; color: #666; margin-bottom: 15px;">
            Please verify the bin status and provide a current photo before marking as collected.
          </p>
          
          <mat-form-field appearance="outline" class="full-width">
            <mat-label>Feedback/Notes</mat-label>
            <textarea matInput [(ngModel)]="feedback" rows="3" placeholder="e.g. Bin threshold met, Area accessible..."></textarea>
          </mat-form-field>
          
          <div class="photo-upload">
            <label for="collector-photo" class="upload-label">
              <mat-icon style="font-size: 40px; width: 40px; height: 40px; margin-bottom: 10px;">add_a_photo</mat-icon>
              <span>{{selectedFile ? selectedFile.name : 'Take/Upload Photo of Bin'}}</span>
              <p *ngIf="!selectedFile" style="font-size: 0.8em; color: #888;">Required for verification</p>
            </label>
            <input type="file" id="collector-photo" (change)="onFileSelected($event)" accept="image/*" style="display: none;">
          </div>
        </div>

        <!-- Feedback Display Section (for Admin and History) -->
        <div *ngIf="data.report.collector_feedback || data.report.collector_image" class="feedback-display" style="border-left: 4px solid #4caf50; padding-left: 15px; margin-top: 20px;">
          <h3 style="color: #2e7d32;">Collector Verification Result</h3>
          <p *ngIf="data.report.collector_feedback"><strong>Note:</strong> {{data.report.collector_feedback}}</p>
          <div *ngIf="data.report.collector_image" style="margin-top: 10px;">
            <p><strong>Real-time Proof:</strong></p>
            <img [src]="data.report.collector_image" alt="Verification photo" class="main-photo" (click)="zoomCollectorPhoto = !zoomCollectorPhoto" [class.zoomed]="zoomCollectorPhoto">
          </div>
        </div>

        <!-- Admin Action Section (for Awarding/Deducting Points) -->
        <div *ngIf="data.role === 'admin' && data.report.status === 'collected'" class="admin-feedback-section" style="margin-top: 25px; padding: 15px; background: #e8f5e9; border-radius: 8px;">
           <h3 style="margin-top: 0;">Point Management</h3>
           <p style="font-size: 0.9em;">Based on collector feedback, you can reward or penalize the citizen.</p>
           <mat-form-field appearance="outline" class="full-width">
             <mat-label>Admin Comments (Optional)</mat-label>
             <textarea matInput [(ngModel)]="adminFeedback" rows="2"></textarea>
           </mat-form-field>
           <div style="display: flex; gap: 10px;">
              <button mat-flat-button color="primary" style="flex: 1;" (click)="onSubmitAdmin(true)">
                <mat-icon>thumb_up</mat-icon> Reward (+10 pts)
              </button>
              <button mat-flat-button color="warn" style="flex: 1;" (click)="onSubmitAdmin(false)">
                <mat-icon>thumb_down</mat-icon> Penalize (-5 pts)
              </button>
           </div>
        </div>
      </div>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button mat-dialog-close>Close</button>
      <button mat-raised-button color="primary" *ngIf="data.role === 'collector' && data.report.status === 'assigned'" 
              [disabled]="!feedback || !selectedFile" (click)="onSubmitCollector()">
        Confirm Collection
      </button>
    </mat-dialog-actions>
  `,
  styles: [`
    .full-width { width: 100%; }
    .main-photo { width: 100%; max-height: 250px; object-fit: cover; border-radius: 8px; cursor: pointer; border: 1px solid #ddd; transition: all 0.3s ease; }
    .main-photo:hover { opacity: 0.9; }
    .main-photo.zoomed { max-height: 80vh; transform: none; object-fit: contain; background: black; }
    .badge { padding: 4px 10px; border-radius: 12px; font-size: 0.85em; font-weight: 500; }
    .pending { background: #fff3cd; color: #856404; }
    .assigned { background: #cce5ff; color: #004085; }
    .collected { background: #d4edda; color: #155724; }
    .verified { background: #d1ecf1; color: #0c5460; }
    .rejected { background: #f8d7da; color: #721c24; }
    .upload-label { border: 2px dashed #3f51b5; padding: 25px; display: flex; flex-direction: column; align-items: center; cursor: pointer; border-radius: 8px; margin: 15px 0; background: #f5f6ff; transition: background 0.2s; }
    .upload-label:hover { background: #ebedff; }
    .hint { font-size: 0.8em; color: #888; text-align: center; margin-top: 5px; }
  `]
})
export class ReportDetailsComponent {
  feedback: string = '';
  selectedFile: File | null = null;
  adminFeedback: string = '';
  zoomPhoto = false;
  zoomCollectorPhoto = false;

  constructor(
    public dialogRef: MatDialogRef<ReportDetailsComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    if (data.report.collector_feedback) {
      this.feedback = data.report.collector_feedback;
    }
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
    }
  }

  onSubmitCollector() {
    this.dialogRef.close({
      action: 'collected',
      feedback: this.feedback,
      image: this.selectedFile
    });
  }

  onSubmitAdmin(isAccurate: boolean) {
    this.dialogRef.close({
      action: 'verify',
      isAccurate: isAccurate,
      feedback: this.adminFeedback
    });
  }
}
