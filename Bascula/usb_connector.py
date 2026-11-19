import random
import threading
import time
from .models import RegistroPeso

class BasculaSimulador:
    def __init__(self):
        self.is_connected = False
        self.peso_actual = 0.0
        self.corriendo = False
        self.intervalo = 2.0
        self.min_peso = 0.5
        self.max_peso = 5.0
        self.variacion_maxima = 0.3
        self.ultimo_peso = 0.0

    def conectar(self):
        if self.is_connected:
            return True, "Ya conectado"
        self.is_connected = True
        self.corriendo = True
        self.peso_actual = random.uniform(self.min_peso, self.max_peso)
        self.lectura_thread = threading.Thread(target=self._simular_lecturas, daemon=True)
        self.lectura_thread.start()
        return True, "Simulador conectado"

    def desconectar(self):
        self.corriendo = False
        self.is_connected = False
        return True, "Simulador desconectado"

    def _simular_lecturas(self):
        contador = 0
        while self.corriendo and self.is_connected:
            variacion = random.uniform(-self.variacion_maxima, self.variacion_maxima)
            nuevo_peso = self.peso_actual + variacion
            nuevo_peso = max(self.min_peso, min(self.max_peso, nuevo_peso))
            self.peso_actual = nuevo_peso
            self.ultimo_peso = round(self.peso_actual, 3)
            contador += 1
            if contador % 3 == 0:
                try:
                    RegistroPeso.objects.create(peso=self.ultimo_peso)
                except Exception:
                    pass
            time.sleep(self.intervalo)

    def obtener_peso(self):
        return self.ultimo_peso

simulador = BasculaSimulador()