# test.py
import unittest
from optimizer import LogisticsOptimizer

class TestOptimizer(unittest.TestCase):
    def test_transport(self):
        opt = LogisticsOptimizer([{'capacity': 1000, 'location': (0, 0)}],
                                 [{'demand': 500, 'location': (1, 1)}])
        sol = opt.solve_transportation_problem()
        self.assertIsInstance(sol, dict)

if __name__ == '__main__':
    unittest.main()
