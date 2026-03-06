import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WasteReportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'waste_reports'
        self.room_group_name = 'waste_reports_group'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (if client sends data)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'report_update',
                'message': message
            }
        )

    # Receive message from room group
    async def report_update(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

class TrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'tracking_group'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Expecting { 'collector_id': 1, 'lat': -1.2, 'lng': 36.8 }
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'location_update',
                'data': data
            }
        )

    async def location_update(self, event):
        await self.send(text_data=json.dumps(event['data']))

