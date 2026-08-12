import serial
import serial.tools.list_ports
import threading
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class BasculaUSB:
    def __init__(self):
        self.serial = None
        self.is_connected = False
        self.puerto = None
        self.lectura_thread = None
        self.corriendo = False
        
    def listar_puertos(self):
        """Lista todos los puertos USB disponibles"""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def conectar(self, puerto, baudrate=115200):
        """Conectar a la báscula por USB"""
        try:
            self.serial = serial.Serial(
                port=puerto,
                baudrate=baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            self.is_connected = True
            self.puerto = puerto
            self.corriendo = True
            
            # Iniciar hilo de lectura
            self.lectura_thread = threading.Thread(target=self._leer_datos)
            self.lectura_thread.daemon = True
            self.lectura_thread.start()
            
            return True, "Conectado correctamente"
        except Exception as e:
            return False, f"Error al conectar: {str(e)}"
    
    def desconectar(self):
        """Desconectar la báscula"""
        self.corriendo = False
        self.is_connected = False
        if self.serial and self.serial.is_open:
            self.serial.close()
        return True, "Desconectado correctamente"
    
    def _leer_datos(self):
        """Hilo para leer datos de la báscula continuamente"""
        while self.corriendo and self.is_connected:
            try:
                if self.serial and self.serial.in_waiting > 0:
                    # Leer línea de datos
                    linea = self.serial.readline().decode('utf-8').strip()
                    if linea:
                        # Procesar el peso (formato depende de la báscula)
                        peso = self._procesar_peso(linea)
                        if peso is not None:
                            # Enviar a WebSocket
                            self._enviar_peso(peso)
            except Exception as e:
                print(f"Error al leer datos: {e}")
                break
    
    def _procesar_peso(self, linea):
        """Procesar la línea de datos de la báscula"""
        # Aquí debes adaptar según el formato de tu báscula
        # Ejemplo: formato "   0.000 kg"
        try:
            # Buscar número en la línea
            import re
            numeros = re.findall(r'[-+]?\d*\.?\d+', linea)
            if numeros:
                return float(numeros[0])
        except:
            pass
        return None
    
    def _enviar_peso(self, peso):
        """Enviar peso a través de WebSocket"""
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "peso_group",
                {
                    'type': 'peso_update',
                    'peso': peso,
                    'fecha': None  # Se agrega automáticamente en el consumer
                }
            )
        except Exception as e:
            print(f"Error al enviar peso: {e}")

# Instancia global
bascula = BasculaUSB()