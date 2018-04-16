# from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
#
# class WebsocketRecieve(AsyncWebsocketConsumer):
#     groups = ["broadcast"]
#
#     async def connect(self):
#         # Called on connection.
#         # To accept the connection call:
#         await self.accept()
#
#     async def receive(self, text_data=None, bytes_data=None):
#         # Called with either text_data or bytes_data for each frame
#         await self.send(text_data="Hello world!")
#
#     async def disconnect(self, close_code):
#         # Called when the socket closes
#         pass
#
#
# class WebsocketSend(WebsocketConsumer):
#
#     def turn_on_led(self, colour):
#         # Called by 'leds' view
#         self.send(text_data=colour)