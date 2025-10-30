# proyecto_logistica
1️⃣ Copiar el proyecto

Copiar la carpeta del proyecto en D:\Usuario\Desktop\OBRA_MAESTRA\Programacion\proyecto_logistica (ya la tenés).

Abrir CMD o PowerShell y moverse a la carpeta:

cd D:\Usuario\Desktop\OBRA_MAESTRA\Programacion\proyecto_logistica

2️⃣ Crear un entorno virtual (opcional pero recomendado)
python -m venv venv


Activar el entorno:

venv\Scripts\activate


Notarás que el prompt de CMD cambia a (venv).

3️⃣ Instalar dependencias

Con el entorno virtual activado, instalar todos los paquetes necesarios:

pip install numpy pandas simpy scikit-learn plotly streamlit


Opcional: instalar pytest si querés correr tests unitarios:

pip install pytest

4️⃣ Probar que funcione el código principal

Para probar la simulación desde consola:

python main.py


Debe mostrar algo como:

{'performance': 'Entregas: 30, Distancia: 500', 'insights': 'Optimización reduce costos en 15%.'}


Para correr tests unitarios:

python test.py


Debe pasar sin errores.

5️⃣ Correr el dashboard

Con el entorno virtual activado, ejecutar:

streamlit run dashboard.py


Se abrirá el navegador con el dashboard.

Usar el panel lateral para seleccionar días de simulación y presionar Ejecutar Simulación.