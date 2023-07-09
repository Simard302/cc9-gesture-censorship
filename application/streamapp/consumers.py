from channels.generic.websocket import AsyncWebsocketConsumer

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Process the received video frame here
        # You can access the frame data using `text_data` variable
        # For example, you can save the frame to a file or perform some image processing
        
        # Replace this with your actual processing code
        # This example simply broadcasts the received frame to all connected clients
        await self.channel_layer.group_send(
            'stream_group',
            {'type': 'stream_message', 'data': text_data}
        )

    async def stream_message(self, event):
        await self.send(event['data'])
