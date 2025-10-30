# test.py
import unittest  # Importa el framework de pruebas unitarias
from optimizer import LogisticsOptimizer  # Importa la clase a probar

class TestOptimizer(unittest.TestCase):  # Define clase de pruebas para el optimizador
    def test_transport(self):  # Define prueba para el problema de transporte
        opt = LogisticsOptimizer([{'capacity': 1000, 'location': (0, 0)}],  # Crea optimizador con un almacén
                                 [{'demand': 500, 'location': (1, 1)}])  # Crea optimizador con una tienda
        sol = opt.solve_transportation_problem()  # Ejecuta solución del problema de transporte
        self.assertIsInstance(sol, dict)  # Verifica que la solución sea un diccionario

if __name__ == '__main__':
    unittest.main()  # Ejecuta todas las pruebas definidas