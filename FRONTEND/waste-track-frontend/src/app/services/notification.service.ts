import { Injectable } from '@angular/core';
import { getMessaging, getToken, onMessage } from "firebase/messaging";
import { initializeApp } from "firebase/app";
import { firebaseConfig } from "../firebase-config";
import { HttpClient } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';


import { environment } from '../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class NotificationService {
    private messaging;
    private apiUrl = `${environment.apiUrl}/auth/fcm/register/`;

    constructor(private http: HttpClient, private snackBar: MatSnackBar) {
        try {
            const app = initializeApp(firebaseConfig);
            this.messaging = getMessaging(app);
        } catch (e) {
            console.error("Firebase initialization failed:", e);
        }
    }

    requestPermission() {
        if (!this.messaging) return;

        getToken(this.messaging, { vapidKey: 'YOUR_PUBLIC_VAPID_KEY' })
            .then((currentToken) => {
                if (currentToken) {
                    console.log("FCM Token:", currentToken);
                    this.saveToken(currentToken);
                } else {
                    console.log('No registration token available. Request permission to generate one.');
                }
            }).catch((err) => {
                console.log('An error occurred while retrieving token. ', err);
            });
    }

    private saveToken(token: string) {
        this.http.post(this.apiUrl, { registration_token: token }).subscribe({
            next: () => console.log("Token saved to backend"),
            error: (err) => console.error("Error saving token:", err)
        });
    }

    listen() {
        if (!this.messaging) return;
        onMessage(this.messaging, (payload) => {
            console.log('Message received. ', payload);
            this.snackBar.open(`${payload.notification?.title}: ${payload.notification?.body}`, 'Close', { duration: 10000 });
        });
    }
}
