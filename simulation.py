# simulation.py
import simpy
import random

class RealTimeLogistics:
    def __init__(self, env, optimizer):
        self.env = env
        self.optimizer = optimizer
        self.performance_metrics = {
            'deliveries_completed': 0,
            'total_distance': 0,
            'delivery_times': []
        }

    def delivery_process(self, route):
        start_time = self.env.now
        for stop in route:
            # Tiempo de viaje aleatorio
            yield self.env.timeout(random.normalvariate(60, 10))
            # Tiempo de descarga aleatorio
            yield self.env.timeout(random.expovariate(1/30))
        end_time = self.env.now
        self.performance_metrics['deliveries_completed'] += 1
        self.performance_metrics['delivery_times'].append(end_time - start_time)

    def operate_system(self, days):
        for day in range(days):
            routes = self.optimizer.vehicle_routing_with_time_windows()
            for route in routes:
                self.env.process(self.delivery_process(route))
            yield self.env.timeout(24*60)  # 1 día en minutos
