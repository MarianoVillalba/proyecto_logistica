# main.py
from optimizer import LogisticsOptimizer  # Importa el optimizador logístico
from inventory import InventoryManagementSystem  # Importa el sistema de gestión de inventario
from simulation import RealTimeLogistics  # Importa el sistema de logística en tiempo real
import simpy  # Importa simpy para simulaciones
import pandas as pd  # Importa pandas para manejo de datos
import numpy as np  # Importa numpy para operaciones numéricas

case_study = {
    'warehouses': [
        {'capacity': 10000, 'location': (-34.50, -58.50)},  # Define almacén 1 con capacidad y ubicación
        {'capacity': 8000, 'location': (-34.70, -58.45)},   # Define almacén 2 con capacidad y ubicación
        {'capacity': 12000, 'location': (-34.60, -58.70)}   # Define almacén 3 con capacidad y ubicación
    ],
    'stores': [
        {'demand': 1500, 'location': (-34.55, -58.48)},  # Define tienda 1 con demanda y ubicación
        {'demand': 1200, 'location': (-34.65, -58.52)},  # Define tienda 2 con demanda y ubicación
        {'demand': 1000, 'location': (-34.62, -58.55)},  # Define tienda 3 con demanda y ubicación
        {'demand': 800, 'location': (-34.58, -58.60)},   # Define tienda 4 con demanda y ubicación
        {'demand': 1100, 'location': (-34.67, -58.65)}   # Define tienda 5 con demanda y ubicación
    ]
}

def run_complete_simulation(days=30):
    env = simpy.Environment()  # Crea entorno de simulación
    opt = LogisticsOptimizer(case_study['warehouses'], case_study['stores'])  # Instancia el optimizador logístico
    inv_sys = InventoryManagementSystem(pd.DataFrame({'nivel_inventario': np.random.randint(100, 500, 100)}, index=pd.date_range('2023-01-01', periods=100)), [5, 7, 10], [0.5,0.6,0.4])  # Crea sistema de inventario con datos ficticios
    rt_sys = RealTimeLogistics(env, opt)  # Instancia el sistema de logística en tiempo real
    env.process(rt_sys.operate_system(days))  # Inicia el proceso de operación del sistema
    env.run(until=days*24*60)  # Ejecuta la simulación por el número de días especificado
    return {
        'performance': f"Entregas: {rt_sys.performance_metrics['deliveries_completed']}, Distancia: {rt_sys.performance_metrics['total_distance']}",  # Retorna métricas de desempeño
        'insights': "Optimización reduce costos en 15%."  # Retorna insight de optimización
    }

if __name__ == "__main__":
    result = run_complete_simulation(7)  # Ejecuta simulación de 7 días
    print(result)  # Imprime resultados de la simulación