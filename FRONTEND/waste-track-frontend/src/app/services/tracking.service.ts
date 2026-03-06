import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class TrackingService {
    private socket: WebSocket | null = null;
    public locationUpdates$ = new Subject<any>();

    connect() {
        this.socket = new WebSocket('ws://127.0.0.1:8000/ws/tracking/');

        this.socket.onmessage = (event) => {
            const data = json.parse(event.data);
            this.locationUpdates$.next(data);
        };

        this.socket.onclose = () => {
            console.log("Tracking socket closed. Reconnecting...");
            setTimeout(() => this.connect(), 5000);
        };
    }

    sendLocation(collectorId: number, lat: number, lng: number) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({ collector_id: collectorId, lat, lng }));
        }
    }
}

// Global helper for JSON parsing safely if needed
const json = {
    parse: (text: string) => {
        try {
            return JSON.parse(text);
        } catch (e) {
            return null;
        }
    }
};
