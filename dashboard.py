# dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from optimizer import LogisticsOptimizer
from inventory import InventoryManagementSystem
from simulation import RealTimeLogistics
import simpy

# -------------------------
# Datos de ejemplo del caso de estudio
# -------------------------
case_study = {
    'warehouses': [
        {'id': 'WH_Norte', 'capacity': 10000, 'location': (-34.50, -58.50)},
        {'id': 'WH_Sur', 'capacity': 8000, 'location': (-34.70, -58.45)},
        {'id': 'WH_Oeste', 'capacity': 12000, 'location': (-34.60, -58.70)}
    ],
    'stores': [
        {'id': 'SUPER_01', 'demand': 1500, 'location': (-34.55, -58.48)},
        {'id': 'SUPER_02', 'demand': 1200, 'location': (-34.65, -58.52)},
        {'id': 'SUPER_03', 'demand': 1000, 'location': (-34.60, -58.55)}
    ]
}

# -------------------------
# Configuración de Streamlit
# -------------------------
st.set_page_config(page_title='Logistics Dashboard', layout='wide')
st.title('Sistema de Optimización Logística Inteligente')

# -------------------------
# Inicializar sistemas
# -------------------------
opt = LogisticsOptimizer(case_study['warehouses'], case_study['stores'])

# Inventarios de ejemplo
dates = pd.date_range('2023-01-01', periods=30)
inv_df = pd.DataFrame({
    'fecha': np.tile(dates, len(case_study['warehouses'])),
    'nivel_inventario': np.random.randint(500, 1500, size=30*len(case_study['warehouses'])),
    'almacen': np.repeat([wh['id'] for wh in case_study['warehouses']], 30)
}).set_index('fecha')

inv_sys = InventoryManagementSystem(inv_df, [5,7,10], [0.5,0.6,0.4])

# -------------------------
# Panel lateral
# -------------------------
days = st.sidebar.slider('Días de simulación', 1, 30, 7)
run_sim = st.sidebar.button('Ejecutar Simulación')

# -------------------------
# Simulación
# -------------------------
if run_sim:
    env = simpy.Environment()
    rt_sys = RealTimeLogistics(env, opt)

    # Dummy simulation para demo
    def dummy_operate_system(env, rt_sys, days):
        for day in range(days):
            yield env.timeout(24*60)
            rt_sys.performance_metrics['deliveries_completed'] += 10
            rt_sys.performance_metrics['total_distance'] += 200

    env.process(dummy_operate_system(env, rt_sys, days))
    env.run()
    metrics = rt_sys.performance_metrics
else:
    metrics = {'deliveries_completed': 120, 'total_distance': 5000}

# -------------------------
# Métricas principales
# -------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric('Entregas completadas', metrics['deliveries_completed'])
col2.metric('Distancia total', f"{metrics['total_distance']} km")
col3.metric('Nivel de servicio', '98%')
col4.metric('Costo total', '$12,430')

# -------------------------
# Rutas
# -------------------------
st.subheader('Rutas de entrega')
routes = [
    [{'lat': -34.50, 'lon': -58.50}, {'lat': -34.55, 'lon': -58.48}],
    [{'lat': -34.70, 'lon': -58.45}, {'lat': -34.65, 'lon': -58.52}]
]

for i, r in enumerate(routes):
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        lat=[p['lat'] for p in r],
        lon=[p['lon'] for p in r],
        mode='lines+markers',
        name=f'Ruta {i+1}'
    ))
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=11,
        mapbox_center={"lat": -34.60, "lon": -58.50},
        margin={"l":0,"r":0,"t":0,"b":0}
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Inventarios
# -------------------------
st.subheader('Niveles de Inventario')
fig = px.line(inv_df, x=inv_df.index, y='nivel_inventario', color='almacen',
              title='Evolución de Inventarios por Almacén')
st.plotly_chart(fig, use_container_width=True)
