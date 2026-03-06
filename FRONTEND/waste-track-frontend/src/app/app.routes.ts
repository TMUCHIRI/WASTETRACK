import { Routes } from '@angular/router';
import { LandingComponent } from './components/landing/landing.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { PasswordResetComponent } from './components/password-reset/password-reset.component';
import { ReportWasteComponent } from './components/report-waste/report-waste.component';
import { authGuard } from './guards/auth.guard';
import { collectorGuard } from './guards/collector.guard';
import { adminGuard } from './guards/admin.guard';
import { CollectorDashboardComponent } from './components/dashboards/collector/collector-dashboard.component';
import { AdminDashboardComponent } from './components/dashboards/admin/admin-dashboard.component';

import { DashboardComponent } from './components/dashboard/dashboard.component';

export const routes: Routes = [
  { path: '', redirectTo: '/landing', pathMatch: 'full' },
  { path: 'landing', component: LandingComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'forgot-password', component: PasswordResetComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [authGuard] },
  { path: 'report', component: ReportWasteComponent, canActivate: [authGuard] },
  { path: 'collector-dashboard', component: CollectorDashboardComponent, canActivate: [collectorGuard] },
  { path: 'admin-dashboard', component: AdminDashboardComponent, canActivate: [adminGuard] },
  { path: '**', redirectTo: '/landing' }
];

