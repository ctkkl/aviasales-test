import json
import unittest
from envi import Request
from datetime import date
from controllers import RoutesController


class ControllersTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_get_routes(self):
        """
        Проверка контроллера на получение полетов и сортировки
        :return:
        """
        r = Request()
        r.set('source', 'DXB')
        r.set('destination', 'BKK')
        r.set('departure_date', date(2018, 10, 27))

        result = json.loads(RoutesController().get_routes(r)).get('result')
        self.assertEqual(102, len(result['routes']))

        r.set('departure_date', date(2018, 10, 22))

        result = json.loads(RoutesController().get_routes(r)).get('result')
        self.assertEqual(200, len(result['routes']))

        r.set('order_field', 'price')
        r.set('order_value', 'asc')
        r.set('limit', 1)
        result = json.loads(RoutesController().get_routes(r)).get('result')
        self.assertEqual(1, len(result['routes']))

