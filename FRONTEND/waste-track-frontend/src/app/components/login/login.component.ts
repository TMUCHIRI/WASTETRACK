import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { AuthService } from '../../services/auth.service';

import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, MatIconModule, MatFormFieldModule, MatInputModule, MatButtonModule, FormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  loginData = { identifier: '', password: '' };
  otp = '';
  step: 'login' | 'otp' = 'login';
  showPassword = false;
  isLoading = false;
  errorMessage = '';

  constructor(private authService: AuthService, private router: Router) { }

  onLogin(data: { identifier: string; password: string }) {
    this.isLoading = true;
    this.errorMessage = '';

    this.authService.login(data.identifier, data.password).subscribe({
      next: (response) => {
        this.isLoading = false;
        if (response.requires_2fa) {
          this.step = 'otp';
        } else {
          this.navigateToDashboard();
        }
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message;
      }
    });
  }

  onVerifyOtp() {
    this.isLoading = true;
    this.errorMessage = '';
    this.authService.verifyOtp(this.loginData.identifier, this.otp).subscribe({
      next: () => {
        this.isLoading = false;
        this.navigateToDashboard();
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message;
      }
    });
  }

  private navigateToDashboard() {
    const role = this.authService.getUserRole();
    switch (role) {
      case 'admin':
        this.router.navigate(['/admin-dashboard']);
        break;
      case 'collector':
        this.router.navigate(['/collector-dashboard']);
        break;
      case 'resident':
      case 'citizen':
        this.router.navigate(['/dashboard']);
        break;
      default:
        this.router.navigate(['/landing']);
        break;
    }
  }
}
