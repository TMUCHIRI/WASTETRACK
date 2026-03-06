import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

import { AuthService } from '../../services/auth.service';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule, FormsModule, MatFormFieldModule, MatInputModule, MatButtonModule, MatIconModule, RouterModule],
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent {
  constructor(private authService: AuthService, private router: Router) { }

  get isLoggedIn(): boolean {
    return this.authService.isLoggedIn();
  }

  goToDashboard() {
    const role = this.authService.getUserRole();
    if (role === 'admin') this.router.navigate(['/admin-dashboard']);
    else if (role === 'collector') this.router.navigate(['/collector-dashboard']);
    else this.router.navigate(['/dashboard']);
  }

  onContactSubmit() {
    console.log('Contact form submitted');
  }
}
