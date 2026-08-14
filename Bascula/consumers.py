import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import RegistroPeso

class PesoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket conectado")

    async def disconnect(self, close_code):
        print("WebSocket desconectado")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            peso = data.get('peso')
            
            if peso is not None and peso > 0:
                registro = await self.guardar_peso(peso)
                
                await self.send(text_data=json.dumps({
                    'peso': peso,
                    'fecha': registro.fecha_registro.strftime('%d/%m/%Y %H:%M:%S') if registro else None,
                    'id': registro.id if registro else None
                }))
        except:
            pass

    @database_sync_to_async
    def guardar_peso(self, peso):
        return RegistroPeso.objects.create(peso=peso)