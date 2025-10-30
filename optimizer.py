import numpy as np
import networkx as nx
from pulp import LpProblem, LpVariable, lpSum, LpMinimize
from geopy.distance import geodesic

class LogisticsOptimizer:
    def __init__(self, warehouses, stores):
        self.warehouses = warehouses
        self.stores = stores
        self.distance_matrix = self.calculate_distance_matrix()
        self.G = self.build_network_graph()

    def calculate_distance_matrix(self):
        wh_locs = [wh['location'] for wh in self.warehouses]
        store_locs = [store['location'] for store in self.stores]
        matrix = np.zeros((len(wh_locs), len(store_locs)))
        for i, wh in enumerate(wh_locs):
            for j, store in enumerate(store_locs):
                matrix[i][j] = geodesic(wh, store).km
        return matrix

    def build_network_graph(self):
        G = nx.Graph()
        for i, wh in enumerate(self.warehouses):
            G.add_node(f"WH_{i}", capacity=wh['capacity'])
        for i, store in enumerate(self.stores):
            G.add_node(f"STORE_{i}", demand=store['demand'])
        for i in range(len(self.warehouses)):
            for j in range(len(self.stores)):
                G.add_edge(f"WH_{i}", f"STORE_{j}", weight=self.distance_matrix[i][j])
        return G

    def solve_transportation_problem(self):
        prob = LpProblem("Transportation", LpMinimize)
        x = {}
        for i in range(len(self.warehouses)):
            for j in range(len(self.stores)):
                x[i, j] = LpVariable(f"x_{i}_{j}", 0)
        prob += lpSum(self.distance_matrix[i][j] * x[i, j] for i in range(len(self.warehouses)) for j in range(len(self.stores)))
        for i in range(len(self.warehouses)):
            prob += lpSum(x[i, j] for j in range(len(self.stores))) <= self.warehouses[i]['capacity']
        for j in range(len(self.stores)):
            prob += lpSum(x[i, j] for i in range(len(self.warehouses))) >= self.stores[j]['demand']
        prob.solve()
        return {f"x_{i}_{j}": x[i, j].varValue for i in range(len(self.warehouses)) for j in range(len(self.stores))}

    def vehicle_routing_with_time_windows(self):
        routes = self.clarke_wright_savings()
        return self.optimize_route_sequence(routes)

    def clarke_wright_savings(self):
        savings = []
        for i in range(len(self.stores)):
            for j in range(i + 1, len(self.stores)):
                saving = (self.distance_to_warehouse(i) + self.distance_to_warehouse(j) - self.store_distance(i, j))
                savings.append((saving, i, j))
        savings.sort(reverse=True)
        routes = [[i] for i in range(len(self.stores))]
        for saving, i, j in savings:
            route_i = next((r for r in routes if i in r), None)
            route_j = next((r for r in routes if j in r), None)
            if route_i != route_j and len(route_i) + len(route_j) <= 10:
                route_i.extend(route_j)
                routes.remove(route_j)
        return routes

    def optimize_route_sequence(self, routes):
        optimized = []
        for route in routes:
            if route:
                optimized.append(route)  # Simplificado
        return optimized

    def distance_to_warehouse(self, store_idx):
        return min(self.distance_matrix[i][store_idx] for i in range(len(self.warehouses)))

    def store_distance(self, i, j):
        return geodesic(self.stores[i]['location'], self.stores[j]['location']).km

    def get_current_routes(self):
        routes = self.vehicle_routing_with_time_windows()
        return [[{'lat': self.stores[stop]['location'][0], 'lon': self.stores[stop]['location'][1]} for stop in route] for route in routes]