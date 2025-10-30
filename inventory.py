# inventory.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from scipy.optimize import minimize
import numpy as np

class InventoryManagementSystem:
    def __init__(self, historical_data, lead_times, holding_costs):
        self.historical_data = historical_data
        self.lead_times = lead_times
        self.holding_costs = holding_costs
        self.demand_model = self.train_demand_forecaster()

    def train_demand_forecaster(self):
        features = self.create_features(self.historical_data)
        target = self.historical_data['nivel_inventario']
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(features, target)
        return model

    def create_features(self, data):
        features = data.copy()
        # Agregar características temporales
        features['day_of_week'] = features.index.dayofweek
        features['rolling_mean_7'] = features['nivel_inventario'].rolling(7).mean().fillna(0)

        # Codificar columna 'almacen' como números (one-hot)
        if 'almacen' in features.columns:
            features = pd.get_dummies(features, columns=['almacen'])
        
        return features.drop(['nivel_inventario'], axis=1)

    def multi_echelon_inventory_optimization(self):
        def total_cost(levels):
            cost = sum(self.holding_costs[i] * levels[i] for i in range(len(levels)))
            return cost
        result = minimize(total_cost, [100]*len(self.holding_costs),
                          bounds=[(0,1000)]*len(self.holding_costs))
        return result.x

    def get_inventory_status(self):
        dates = pd.date_range('2023-01-01', periods=30)
        return pd.DataFrame({
            'fecha': np.tile(dates, 3),
            'nivel_inventario': np.random.randint(500, 1500, size=30*3),
            'almacen': np.repeat(['WH_Norte','WH_Sur','WH_Oeste'], 30)
        }).set_index('fecha')
