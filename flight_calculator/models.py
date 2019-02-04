import os
from parser import RoutesParser, files_folder
from schemas import RoutesList, Route


def get_routes_from_files() -> list:
    """
    Загрузим маршрутные данные от поставщиков
    :return:
    """
    result = []
    for file_name in os.listdir(files_folder):
        result.extend(RoutesParser()(file_name=file_name))

    return result


# noinspection PyMethodMayBeStatic
class RoutesHandler(object):
    def __init__(self):
        self.get_routes_call = get_routes_from_files

    def validate_routes(self, route: Route, source: str, destination: str, departure_date, passenger: str) -> bool:
        """
        Фильтр маршрутов на те, что нам нужны
        :param route: Экземпляр класса Route
        :param source: Город вылета
        :param destination: Город прилета
        :param departure_date: Дата вылета
        :param passenger: Тип пассажира
        :return:
        """
        if route.source != source and route.destination != destination:
            return False

        if departure_date != route.departure_datetime.date():
            return False

        if passenger == 'adult' and not route.adult_price:
            return False
        if passenger == 'child' and not route.child_price:
            return False
        if passenger == 'infant' and not route.infant_price:
            return False

        return True

    def calculate(self, source: str, destination: str, departure_date, passenger='adult', order_field: str = '',
                  order_value: str = 'asc', limit: int = 0):
        """
        Находим полеты по заданным параметрам у партнеров
        :param source: Город вылета
        :param destination: Город прилета
        :param departure_date: Дата вылета
        :param passenger: Тип пассажира
        :param order_field: поле для сортировки
        :param order_value: asc\desc
        :param limit:
        :return:
        """
        routes_list = RoutesList()
        for route in self.get_routes_call():
            if self.validate_routes(route, source, destination, departure_date, passenger):
                routes_list.routes = route

        if order_field:
            routes_list.sort(order_field, order_value=order_value, limit=limit)

        return routes_list
