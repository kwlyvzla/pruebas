import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import RegistroPeso

class PesoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("peso_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("peso_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        peso = data.get('peso')
        
        if peso is not None:
            # Guardar en la base de datos
            registro = await self.guardar_peso(peso)
            
            # Enviar a todos los clientes conectados
            await self.channel_layer.group_send(
                "peso_group",
                {
                    'type': 'peso_update',
                    'peso': peso,
                    'fecha': registro.fecha_registro.strftime('%d/%m/%Y %H:%M:%S') if registro else None,
                    'id': registro.id if registro else None
                }
            )

    async def peso_update(self, event):
        # Enviar el peso a la interfaz web
        await self.send(text_data=json.dumps({
            'peso': event['peso'],
            'fecha': event['fecha'],
            'id': event['id']
        }))

    @database_sync_to_async
    def guardar_peso(self, peso):
        return RegistroPeso.objects.create(peso=peso)