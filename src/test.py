import expr
import unittest

class TestParser(unittest.TestCase):

    def test_add(self):
        self.assertEqual(expr.evs('2+2'), 4)
        self.assertEqual(expr.evs('2+2+2'), 6)
        self.assertEqual(expr.evs('-(2+2)'), 0)

if __name__ == '__main__':
    unittest.main()
