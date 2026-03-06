import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NotificationService } from './services/notification.service';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'waste-track-frontend';

  constructor(
    private notificationService: NotificationService,
    private authService: AuthService
  ) { }

  ngOnInit() {
    this.authService.currentUser$.subscribe(user => {
      if (user) {
        this.notificationService.requestPermission();
        this.notificationService.listen();
      }
    });
  }
}

