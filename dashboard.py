# dashboard.py
import streamlit as st  # Importa Streamlit para crear la interfaz web
import pandas as pd  # Importa pandas para manipulación de datos
import numpy as np  # Importa numpy para operaciones numéricas
import plotly.express as px  # Importa Plotly Express para gráficos
import plotly.graph_objects as go  # Importa Plotly Graph Objects para gráficos más complejos
from optimizer import LogisticsOptimizer  # Importa el optimizador logístico
from inventory import InventoryManagementSystem  # Importa el sistema de gestión de inventario
from simulation import RealTimeLogistics  # Importa el sistema de logística en tiempo real
import simpy  # Importa simpy para simulaciones

# -------------------------
# Datos de ejemplo del caso de estudio
# -------------------------
case_study = {
    'warehouses': [
        {'id': 'WH_Norte', 'capacity': 10000, 'location': (-34.50, -58.50)},  # Define almacén norte
        {'id': 'WH_Sur', 'capacity': 8000, 'location': (-34.70, -58.45)},     # Define almacén sur
        {'id': 'WH_Oeste', 'capacity': 12000, 'location': (-34.60, -58.70)}   # Define almacén oeste
    ],
    'stores': [
        {'id': 'SUPER_01', 'demand': 1500, 'location': (-34.55, -58.48)},  # Define supermercado 1
        {'id': 'SUPER_02', 'demand': 1200, 'location': (-34.65, -58.52)},  # Define supermercado 2
        {'id': 'SUPER_03', 'demand': 1000, 'location': (-34.60, -58.55)}   # Define supermercado 3
    ]
}

# -------------------------
# Configuración de Streamlit
# -------------------------
st.set_page_config(page_title='Logistics Dashboard', layout='wide')  # Configura la página del dashboard
st.title('Sistema de Optimización Logística Inteligente')  # Establece el título principal

# -------------------------
# Inicializar sistemas
# -------------------------
opt = LogisticsOptimizer(case_study['warehouses'], case_study['stores'])  # Crea instancia del optimizador

# Inventarios de ejemplo
dates = pd.date_range('2023-01-01', periods=30)  # Crea rango de fechas de 30 días
inv_df = pd.DataFrame({
    'fecha': np.tile(dates, len(case_study['warehouses'])),  # Repite fechas para cada almacén
    'nivel_inventario': np.random.randint(500, 1500, size=30*len(case_study['warehouses'])),  # Genera niveles aleatorios
    'almacen': np.repeat([wh['id'] for wh in case_study['warehouses']], 30)  # Asigna nombres de almacenes
}).set_index('fecha')  # Establece fecha como índice

inv_sys = InventoryManagementSystem(inv_df, [5,7,10], [0.5,0.6,0.4])  # Crea sistema de inventario

# -------------------------
# Panel lateral
# -------------------------
days = st.sidebar.slider('Días de simulación', 1, 30, 7)  # Crea control deslizante para días de simulación
run_sim = st.sidebar.button('Ejecutar Simulación')  # Crea botón para ejecutar simulación

# -------------------------
# Simulación
# -------------------------
if run_sim:
    env = simpy.Environment()  # Crea entorno de simulación
    rt_sys = RealTimeLogistics(env, opt)  # Crea sistema de logística en tiempo real

    # Dummy simulation para demo
    def dummy_operate_system(env, rt_sys, days):
        for day in range(days):
            yield env.timeout(24*60)  # Espera un día simulado
            rt_sys.performance_metrics['deliveries_completed'] += 10  # Incrementa entregas completadas
            rt_sys.performance_metrics['total_distance'] += 200  # Incrementa distancia total

    env.process(dummy_operate_system(env, rt_sys, days))  # Inicia proceso de simulación
    env.run()  # Ejecuta simulación
    metrics = rt_sys.performance_metrics  # Obtiene métricas de la simulación
else:
    metrics = {'deliveries_completed': 120, 'total_distance': 5000}  # Métricas por defecto

# -------------------------
# Métricas principales
# -------------------------
col1, col2, col3, col4 = st.columns(4)  # Crea 4 columnas para métricas
col1.metric('Entregas completadas', metrics['deliveries_completed'])  # Muestra métrica de entregas
col2.metric('Distancia total', f"{metrics['total_distance']} km")  # Muestra métrica de distancia
col3.metric('Nivel de servicio', '98%')  # Muestra métrica de nivel de servicio
col4.metric('Costo total', '$12,430')  # Muestra métrica de costo total

# -------------------------
# Rutas
# -------------------------
st.subheader('Rutas de entrega')  # Crea subtítulo para sección de rutas
routes = [
    [{'lat': -34.50, 'lon': -58.50}, {'lat': -34.55, 'lon': -58.48}],  # Define ruta 1
    [{'lat': -34.70, 'lon': -58.45}, {'lat': -34.65, 'lon': -58.52}]   # Define ruta 2
]

for i, r in enumerate(routes):
    fig = go.Figure()  # Crea figura de Plotly
    fig.add_trace(go.Scattermapbox(
        lat=[p['lat'] for p in r],  # Extrae latitudes de la ruta
        lon=[p['lon'] for p in r],  # Extrae longitudes de la ruta
        mode='lines+markers',  # Establece modo con líneas y marcadores
        name=f'Ruta {i+1}'  # Asigna nombre a la ruta
    ))
    fig.update_layout(
        mapbox_style="open-street-map",  # Establece estilo del mapa
        mapbox_zoom=11,  # Establece nivel de zoom
        mapbox_center={"lat": -34.60, "lon": -58.50},  # Establece centro del mapa
        margin={"l":0,"r":0,"t":0,"b":0}  # Establece márgenes
    )
    st.plotly_chart(fig, use_container_width=True)  # Muestra el mapa en el dashboard

# -------------------------
# Inventarios
# -------------------------
st.subheader('Niveles de Inventario')  # Crea subtítulo para sección de inventarios
fig = px.line(inv_df, x=inv_df.index, y='nivel_inventario', color='almacen',
              title='Evolución de Inventarios por Almacén')  # Crea gráfico de líneas de inventarios
st.plotly_chart(fig, use_container_width=True)  # Muestra el gráfico en el dashboard