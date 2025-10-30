# inventory.py
import pandas as pd  # Importa pandas para manipulación de datos
from sklearn.ensemble import RandomForestRegressor  # Importa modelo de Random Forest para pronóstico
from scipy.optimize import minimize  # Importa función de optimización
import numpy as np  # Importa numpy para operaciones numéricas

class InventoryManagementSystem:
    def __init__(self, historical_data, lead_times, holding_costs):
        self.historical_data = historical_data  # Almacena datos históricos de inventario
        self.lead_times = lead_times  # Almacena tiempos de entrega
        self.holding_costs = holding_costs  # Almacena costos de mantenimiento
        self.demand_model = self.train_demand_forecaster()  # Entrena modelo de pronóstico de demanda

    def train_demand_forecaster(self):
        features = self.create_features(self.historical_data)  # Crea características para el modelo
        target = self.historical_data['nivel_inventario']  # Define variable objetivo como nivel de inventario
        model = RandomForestRegressor(n_estimators=100, random_state=42)  # Crea modelo Random Forest
        model.fit(features, target)  # Entrena modelo con características y objetivo
        return model  # Retorna modelo entrenado

    def create_features(self, data):
        features = data.copy()  # Copia datos originales
        # Agregar características temporales
        features['day_of_week'] = features.index.dayofweek  # Añade día de la semana como característica
        features['rolling_mean_7'] = features['nivel_inventario'].rolling(7).mean().fillna(0)  # Añade media móvil de 7 días

        # Codificar columna 'almacen' como números (one-hot)
        if 'almacen' in features.columns:
            features = pd.get_dummies(features, columns=['almacen'])  # Convierte almacenes en variables dummy
        
        return features.drop(['nivel_inventario'], axis=1)  # Elimina columna objetivo y retorna características

    def multi_echelon_inventory_optimization(self):
        def total_cost(levels):
            cost = sum(self.holding_costs[i] * levels[i] for i in range(len(levels)))  # Calcula costo total de mantenimiento
            return cost
        result = minimize(total_cost, [100]*len(self.holding_costs),  # Minimiza función de costo
                          bounds=[(0,1000)]*len(self.holding_costs))  # Define límites para niveles de inventario
        return result.x  # Retorna niveles óptimos de inventario

    def get_inventory_status(self):
        dates = pd.date_range('2023-01-01', periods=30)  # Crea rango de fechas de 30 días
        return pd.DataFrame({
            'fecha': np.tile(dates, 3),  # Repite fechas para 3 almacenes
            'nivel_inventario': np.random.randint(500, 1500, size=30*3),  # Genera niveles aleatorios de inventario
            'almacen': np.repeat(['WH_Norte','WH_Sur','WH_Oeste'], 30)  # Asigna nombres de almacenes
        }).set_index('fecha')  # Establece fecha como índice