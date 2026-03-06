import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { AuthService } from '../../services/auth.service';

import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

import { MatSelectModule } from '@angular/material/select';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, MatIconModule, MatFormFieldModule, MatInputModule, MatButtonModule, MatSelectModule, MatSnackBarModule, FormsModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registerData = {
    first_name: '',
    last_name: '',
    phone: '',
    email: '',
    password: '',
    role: 'citizen'
  };
  showPassword = false;
  isLoading = false;
  errorMessage = '';

  constructor(
    private authService: AuthService,
    private snackBar: MatSnackBar,
    private router: Router
  ) { }

  onRegister(data: any) {
    this.isLoading = true;
    this.errorMessage = '';

    this.authService.register(data).subscribe({
      next: () => {
        this.isLoading = false;
        this.snackBar.open('Registration successful! Please log in.', 'Close', { duration: 5000 });
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message;
        this.snackBar.open(err.message, 'Close', { duration: 5000, panelClass: ['error-snackbar'] });
      }
    });
  }
}
