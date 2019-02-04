from envi import Controller, Request, response_format
from datetime import datetime
from models import RoutesHandler
from schemas import RoutesListSchema, RouteSchema


class RoutesController(Controller):

    @classmethod
    @response_format
    def get_routes(cls, request: Request, **kwargs):
        """
        Отдает варианты маршрутов из точки А в точку Б в определенную дату + сортирует с лимитом по определенному полю
        :param request:
        :return:
        """
        source = str(request.get('source'))
        destination = str(request.get('destination'))
        departure_date = datetime.strptime(str(request.get('departure_date')), '%Y-%m-%d').date()

        limit = int(request.get('limit')) if request.get('limit', None) else 0
        order_field = str(request.get('order_field')) if request.get('order_field', None) else ''
        order_value = str(request.get('order_value')).lower() if request.get('order_value', None) else 'asc'

        flights = RoutesHandler().calculate(source, destination, departure_date, order_field=order_field,
                                            order_value=order_value, limit=limit)
        return RoutesListSchema().dump(flights)

