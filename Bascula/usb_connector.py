import random
import threading
import time
from .models import RegistroPeso

class BasculaSimulador:
    """
    Simulador de bascula con registro automatico
    """
    def __init__(self):
        self.is_connected = False
        self.peso_actual = 0.0
        self.corriendo = False
        self.lectura_thread = None
        self.intervalo = 2.0  # Segundos entre lecturas
        self.min_peso = 0.5
        self.max_peso = 5.0
        self.variacion_maxima = 0.3
        self.ultimo_peso = 0.0
        self.registros_automaticos = True  # Activar registro automatico
        
    def conectar(self):
        """Conectar el simulador"""
        if self.is_connected:
            return True, "Simulador ya esta conectado"
            
        self.is_connected = True
        self.corriendo = True
        self.peso_actual = random.uniform(self.min_peso, self.max_peso)
        
        # Iniciar hilo de simulacion
        self.lectura_thread = threading.Thread(target=self._simular_lecturas)
        self.lectura_thread.daemon = True
        self.lectura_thread.start()
        
        return True, "Simulador conectado - Registro automatico activado"
    
    def desconectar(self):
        """Desconectar el simulador"""
        self.corriendo = False
        self.is_connected = False
        if self.lectura_thread:
            self.lectura_thread.join(timeout=1)
        return True, "Simulador desconectado"
    
    def _simular_lecturas(self):
        """Simular lecturas continuas con registro automatico"""
        contador = 0
        while self.corriendo and self.is_connected:
            try:
                # Generar variacion del peso
                variacion = random.uniform(-self.variacion_maxima, self.variacion_maxima)
                nuevo_peso = self.peso_actual + variacion
                nuevo_peso = max(self.min_peso, min(self.max_peso, nuevo_peso))
                self.peso_actual = nuevo_peso
                self.ultimo_peso = round(self.peso_actual, 3)
                
                # Registrar automaticamente cada 3 lecturas
                contador += 1
                if contador % 3 == 0 and self.registros_automaticos:
                    self._registrar_peso(self.ultimo_peso)
                
                time.sleep(self.intervalo)
                
            except Exception as e:
                print(f"Error en simulacion: {e}")
                break
    
    def _registrar_peso(self, peso):
        """Registrar peso en la base de datos"""
        try:
            RegistroPeso.objects.create(peso=peso)
            print(f"Peso registrado automaticamente: {peso} kg")
        except Exception as e:
            print(f"Error al registrar peso: {e}")
    
    def obtener_peso(self):
        """Obtener el ultimo peso simulado"""
        return self.ultimo_peso
    
    def registrar_peso_manual(self, peso):
        """Registrar un peso manualmente"""
        if peso is not None and peso > 0:
            self._registrar_peso(peso)
            return True
        return False

# Instancia global del simulador
simulador = BasculaSimulador()