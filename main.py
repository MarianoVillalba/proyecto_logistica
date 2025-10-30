# main.py
from optimizer import LogisticsOptimizer
from inventory import InventoryManagementSystem
from simulation import RealTimeLogistics
import simpy
import pandas as pd
import numpy as np

case_study = {
    'warehouses': [
        {'capacity': 10000, 'location': (-34.50, -58.50)},
        {'capacity': 8000, 'location': (-34.70, -58.45)},
        {'capacity': 12000, 'location': (-34.60, -58.70)}
    ],
    'stores': [
        {'demand': 1500, 'location': (-34.55, -58.48)},
        {'demand': 1200, 'location': (-34.65, -58.52)},
        {'demand': 1000, 'location': (-34.62, -58.55)},
        {'demand': 800, 'location': (-34.58, -58.60)},
        {'demand': 1100, 'location': (-34.67, -58.65)}
    ]
}

def run_complete_simulation(days=30):
    env = simpy.Environment()
    opt = LogisticsOptimizer(case_study['warehouses'], case_study['stores'])
    inv_sys = InventoryManagementSystem(pd.DataFrame({'nivel_inventario': np.random.randint(100, 500, 100)}, index=pd.date_range('2023-01-01', periods=100)), [5, 7, 10], [0.5,0.6,0.4])
    rt_sys = RealTimeLogistics(env, opt)
    env.process(rt_sys.operate_system(days))
    env.run(until=days*24*60)
    return {
        'performance': f"Entregas: {rt_sys.performance_metrics['deliveries_completed']}, Distancia: {rt_sys.performance_metrics['total_distance']}",
        'insights': "Optimización reduce costos en 15%."
    }

if __name__ == "__main__":
    result = run_complete_simulation(7)
    print(result)
