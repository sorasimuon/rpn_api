import unittest
import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.list_stack = []

    def tearDownClass(self):
        self.list_stack.clear()

    def test_isValidNumber(self):
        self.assertTrue(app.isValidNumber('45'))
        self.assertTrue(app.isValidNumber(45))
        self.assertFalse(app.isValidNumber('djhf34'))
        self.assertTrue(app.isValidNumber('.45'))

    def test_isOperator(self):
        self.assertTrue(app.isOperand('-'))
        self.assertTrue(app.isOperand('+'))
        self.assertTrue(app.isOperand('*'))
        self.assertTrue(app.isOperand('/'))
        self.assertFalse(app.isOperand('**'))
        self.assertFalse(app.isOperand('+-'))


