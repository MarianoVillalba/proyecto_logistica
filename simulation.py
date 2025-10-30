# simulation.py
import simpy  # Importa simpy para simulaciones basadas en eventos
import random  # Importa random para generar números aleatorios

class RealTimeLogistics:
    def __init__(self, env, optimizer):
        self.env = env  # Almacena el entorno de simulación
        self.optimizer = optimizer  # Almacena el optimizador de logística
        self.performance_metrics = {
            'deliveries_completed': 0,  # Contador de entregas completadas
            'total_distance': 0,  # Acumulador de distancia total recorrida
            'delivery_times': []  # Lista para almacenar tiempos de entrega
        }

    def delivery_process(self, route):
        start_time = self.env.now  # Registra tiempo de inicio de la entrega
        for stop in route:
            # Tiempo de viaje aleatorio
            yield self.env.timeout(random.normalvariate(60, 10))  # Simula tiempo de viaje con distribución normal
            # Tiempo de descarga aleatorio
            yield self.env.timeout(random.expovariate(1/30))  # Simula tiempo de descarga con distribución exponencial
        end_time = self.env.now  # Registra tiempo de finalización
        self.performance_metrics['deliveries_completed'] += 1  # Incrementa contador de entregas
        self.performance_metrics['delivery_times'].append(end_time - start_time)  # Almacena tiempo total de entrega

    def operate_system(self, days):
        for day in range(days):
            routes = self.optimizer.vehicle_routing_with_time_windows()  # Obtiene rutas optimizadas
            for route in routes:
                self.env.process(self.delivery_process(route))  # Inicia proceso de entrega para cada ruta
            yield self.env.timeout(24*60)  # Espera 1 día en minutos antes de la siguiente iteración