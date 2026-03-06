import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { AuthService } from '../../services/auth.service';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-password-reset',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    RouterModule
  ],
  template: `
    <div class="auth-container">
      <div class="container">
        
        <!-- NAVBAR -->
        <div class="navbar-section" style="background: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.1); padding: 20px; width: 100%; border-radius: 8px; margin-bottom: 20px;">
          <div class="navbar-content" style="max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between;">
            <div class="brand-name" routerLink="/landing" style="cursor: pointer;">
              <h1 style="font-size: 1.8rem; color: #0a3d62; margin: 0;">WASTETRACK</h1>
            </div>
            <nav style="display: flex; gap: 15px; align-items: center;">
              <a routerLink="/landing" style="margin: 0 15px; cursor: pointer; font-size: 1rem; color: #555; text-decoration: none;">Home</a>
              <a routerLink="/login" style="margin: 0 15px; cursor: pointer; font-size: 1rem; color: #0a3d62; font-weight: bold; text-decoration: none;">Sign In</a>
            </nav>
          </div>
        </div>

        <div class="auth-form" style="max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
          <h2>Reset Password</h2>
          <p *ngIf="step === 1">Enter your email or phone to receive a verification code.</p>
          <p *ngIf="step === 2">Enter the code sent to you and your new password.</p>

          <div *ngIf="errorMessage" class="error-message">{{ errorMessage }}</div>
          <div *ngIf="successMessage" class="success-message">{{ successMessage }}</div>

          <!-- Step 1: Request Reset -->
          <form *ngIf="step === 1" #requestForm="ngForm" (ngSubmit)="onRequest(identifier)">
            <mat-form-field appearance="outline" class="full-width">
              <mat-label>Email or Phone</mat-label>
              <input matInput [(ngModel)]="identifier" name="identifier" required>
            </mat-form-field>
            <div class="btns">
              <button mat-raised-button color="primary" [disabled]="!requestForm.form.valid || isLoading">
                {{ isLoading ? 'Sending...' : 'Send OTP' }}
              </button>
              <a mat-button routerLink="/login">Back to Login</a>
            </div>
          </form>

          <!-- Step 2: Confirm Reset -->
          <form *ngIf="step === 2" #confirmForm="ngForm" (ngSubmit)="onConfirm()">
            <mat-form-field appearance="outline" class="full-width">
              <mat-label>Verification Code</mat-label>
              <input matInput [(ngModel)]="otp" name="otp" required maxlength="6">
            </mat-form-field>
            <mat-form-field appearance="outline" class="full-width">
              <mat-label>New Password</mat-label>
              <input matInput [type]="showPassword ? 'text' : 'password'" [(ngModel)]="newPassword" name="newPassword" required minlength="6">
              <button mat-icon-button matSuffix (click)="showPassword = !showPassword" type="button">
                <mat-icon>{{showPassword ? 'visibility_off' : 'visibility'}}</mat-icon>
              </button>
            </mat-form-field>
            <div class="btns">
              <button mat-raised-button color="primary" [disabled]="!confirmForm.form.valid || isLoading">
                {{ isLoading ? 'Resetting...' : 'Update Password' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .auth-container { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f5f7fa; }
    .container { width: 100%; max-width: 400px; padding: 20px; }
    .auth-form { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
    h2 { color: #2d3748; margin-bottom: 8px; font-weight: 700; }
    p { color: #718096; margin-bottom: 24px; }
    .full-width { width: 100%; }
    .error-message { color: #e53e3e; margin-bottom: 16px; padding: 12px; background: #fff5f5; border-radius: 6px; font-size: 14px; }
    .success-message { color: #38a169; margin-bottom: 16px; padding: 12px; background: #f0fff4; border-radius: 6px; font-size: 14px; }
    .btns { display: flex; flex-direction: column; gap: 12px; margin-top: 16px; }
    button { height: 48px; border-radius: 8px; font-weight: 600; }
  `]
})
export class PasswordResetComponent {
  step = 1;
  identifier = '';
  otp = '';
  newPassword = '';
  isLoading = false;
  errorMessage = '';
  successMessage = '';
  showPassword = false;

  constructor(private authService: AuthService, private router: Router) { }

  onRequest(id: string) {
    this.isLoading = true;
    this.errorMessage = '';
    this.authService.requestPasswordReset(id).subscribe({
      next: () => {
        this.isLoading = false;
        this.step = 2;
        this.successMessage = 'Verification code sent successfully.';
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message;
      }
    });
  }

  onConfirm() {
    this.isLoading = true;
    this.errorMessage = '';
    const data = {
      identifier: this.identifier,
      otp: this.otp,
      new_password: this.newPassword
    };
    this.authService.resetPasswordConfirm(data).subscribe({
      next: () => {
        this.isLoading = false;
        this.successMessage = 'Password updated successfully! Redirecting to login...';
        setTimeout(() => this.router.navigate(['/login']), 2000);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message;
      }
    });
  }
}
