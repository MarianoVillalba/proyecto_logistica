import numpy as np  # Importa numpy para operaciones numéricas
import networkx as nx  # Importa networkx para trabajar con grafos
from pulp import LpProblem, LpVariable, lpSum, LpMinimize  # Importa herramientas de programación lineal
from geopy.distance import geodesic  # Importa función para calcular distancias geográficas

class LogisticsOptimizer:
    def __init__(self, warehouses, stores):
        self.warehouses = warehouses  # Almacena información de almacenes
        self.stores = stores  # Almacena información de tiendas
        self.distance_matrix = self.calculate_distance_matrix()  # Calcula matriz de distancias
        self.G = self.build_network_graph()  # Construye grafo de la red logística

    def calculate_distance_matrix(self):
        wh_locs = [wh['location'] for wh in self.warehouses]  # Extrae ubicaciones de almacenes
        store_locs = [store['location'] for store in self.stores]  # Extrae ubicaciones de tiendas
        matrix = np.zeros((len(wh_locs), len(store_locs)))  # Inicializa matriz de distancias
        for i, wh in enumerate(wh_locs):
            for j, store in enumerate(store_locs):
                matrix[i][j] = geodesic(wh, store).km  # Calcula distancia en km entre almacén y tienda
        return matrix

    def build_network_graph(self):
        G = nx.Graph()  # Crea grafo no dirigido
        for i, wh in enumerate(self.warehouses):
            G.add_node(f"WH_{i}", capacity=wh['capacity'])  # Añade nodos de almacenes con capacidad
        for i, store in enumerate(self.stores):
            G.add_node(f"STORE_{i}", demand=store['demand'])  # Añade nodos de tiendas con demanda
        for i in range(len(self.warehouses)):
            for j in range(len(self.stores)):
                G.add_edge(f"WH_{i}", f"STORE_{j}", weight=self.distance_matrix[i][j])  # Añade aristas con distancias
        return G

    def solve_transportation_problem(self):
        prob = LpProblem("Transportation", LpMinimize)  # Crea problema de minimización
        x = {}
        for i in range(len(self.warehouses)):
            for j in range(len(self.stores)):
                x[i, j] = LpVariable(f"x_{i}_{j}", 0)  # Crea variables de decisión para envíos
        prob += lpSum(self.distance_matrix[i][j] * x[i, j] for i in range(len(self.warehouses)) for j in range(len(self.stores)))  # Define función objetivo: minimizar distancia total
        for i in range(len(self.warehouses)):
            prob += lpSum(x[i, j] for j in range(len(self.stores))) <= self.warehouses[i]['capacity']  # Restricción: capacidad de almacenes
        for j in range(len(self.stores)):
            prob += lpSum(x[i, j] for i in range(len(self.warehouses))) >= self.stores[j]['demand']  # Restricción: demanda de tiendas
        prob.solve()  # Resuelve el problema
        return {f"x_{i}_{j}": x[i, j].varValue for i in range(len(self.warehouses)) for j in range(len(self.stores))}  # Retorna valores de las variables

    def vehicle_routing_with_time_windows(self):
        routes = self.clarke_wright_savings()  # Genera rutas iniciales con algoritmo de ahorros
        return self.optimize_route_sequence(routes)  # Optimiza secuencia de rutas

    def clarke_wright_savings(self):
        savings = []
        for i in range(len(self.stores)):
            for j in range(i + 1, len(self.stores)):
                saving = (self.distance_to_warehouse(i) + self.distance_to_warehouse(j) - self.store_distance(i, j))  # Calcula ahorro al combinar rutas
                savings.append((saving, i, j))
        savings.sort(reverse=True)  # Ordena ahorros de mayor a menor
        routes = [[i] for i in range(len(self.stores))]  # Inicia con rutas individuales
        for saving, i, j in savings:
            route_i = next((r for r in routes if i in r), None)  # Encuentra ruta que contiene tienda i
            route_j = next((r for r in routes if j in r), None)  # Encuentra ruta que contiene tienda j
            if route_i != route_j and len(route_i) + len(route_j) <= 10:  # Verifica factibilidad de combinación
                route_i.extend(route_j)  # Combina rutas
                routes.remove(route_j)  # Elimina ruta combinada
        return routes

    def optimize_route_sequence(self, routes):
        optimized = []
        for route in routes:
            if route:
                optimized.append(route)  # Añade ruta sin optimización adicional (simplificado)
        return optimized

    def distance_to_warehouse(self, store_idx):
        return min(self.distance_matrix[i][store_idx] for i in range(len(self.warehouses)))  # Calcula distancia mínima a cualquier almacén

    def store_distance(self, i, j):
        return geodesic(self.stores[i]['location'], self.stores[j]['location']).km  # Calcula distancia entre dos tiendas

    def get_current_routes(self):
        routes = self.vehicle_routing_with_time_windows()  # Obtiene rutas optimizadas
        return [[{'lat': self.stores[stop]['location'][0], 'lon': self.stores[stop]['location'][1]} for stop in route] for route in routes]  # Convierte a formato coordenadas