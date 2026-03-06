// src/app/services/auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, BehaviorSubject, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { Router } from '@angular/router';

interface User {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  role: string;
}

interface LoginResponse {
  success: boolean;
  token?: string;
  user?: User;
  message?: string;
  requires_2fa?: boolean;
}

interface RegisterResponse {
  success: boolean;
  message: string;
  user?: User;
  token?: string;
}

import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl; // Django backend
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient, private router: Router) {
    const savedUser = localStorage.getItem('user_data');
    if (savedUser) {
      try {
        this.currentUserSubject.next(JSON.parse(savedUser));
      } catch (e) {
        localStorage.removeItem('user_data');
      }
    }
  }


  login(identifier: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/auth/login/`, {
      identifier,
      password
    }).pipe(
      tap(response => {
        // We don't save token here if 2FA is required
        if (response.success && response.token && response.user && !response.requires_2fa) {
          this.handleAuthSuccess(response.token, response.user);
        }
      }),
      catchError(this.handleError)
    );
  }

  verifyOtp(identifier: string, otp: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/auth/verify-otp/`, {
      identifier,
      otp
    }).pipe(
      tap(response => {
        if (response.success && response.token && response.user) {
          this.handleAuthSuccess(response.token, response.user);
        }
      }),
      catchError(this.handleError)
    );
  }

  private handleAuthSuccess(token: string, user: User) {
    localStorage.setItem('token', token);
    localStorage.setItem('user_role', user.role);
    localStorage.setItem('user_data', JSON.stringify(user));
    this.currentUserSubject.next(user);
  }


  requestPasswordReset(identifier: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/password-reset/`, { identifier }).pipe(
      catchError(this.handleError)
    );
  }

  resetPasswordConfirm(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/password-reset-confirm/`, data).pipe(
      catchError(this.handleError)
    );
  }

  register(userData: any): Observable<RegisterResponse> {
    return this.http.post<RegisterResponse>(`${this.apiUrl}/auth/register/`, userData).pipe(
      catchError(this.handleError)
    );
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('user_data');
    this.currentUserSubject.next(null);
    this.router.navigate(['/login']);
  }


  isLoggedIn(): boolean {
    return !!localStorage.getItem('token');
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  getUserRole(): string {
    return localStorage.getItem('user_role') || 'citizen';
  }


  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/users/`).pipe(
      catchError(this.handleError)
    );
  }

  updateUserRole(userId: number, role: string): Observable<User> {
    return this.http.patch<User>(`${this.apiUrl}/users/${userId}/role/`, { role }).pipe(
      catchError(this.handleError)
    );
  }


  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An error occurred. Please try again.';
    if (error.error instanceof ErrorEvent) {
      errorMessage = error.error.message;
    } else {
      errorMessage = error.error?.message || error.error?.error || 'Server error';
    }
    return throwError(() => new Error(errorMessage));
  }
}