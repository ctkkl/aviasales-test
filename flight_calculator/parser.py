import os
from abc import abstractmethod
import xml.etree.ElementTree as Et
from schemas import FlightPriceSchema, FlightPrice, FlightPartSchema, FlightPart, Route, RoutesList
from collections import defaultdict

files_folder = os.getenv('FILES_FOLDER', 'files/')


class RoutesParser(object):

    def __call__(self, *args, **kwargs):
        try:
            file_name: str = kwargs.get('file_name')
            file_type = file_name.lower().split('.')[1]
        except Exception as er:
            # TODO log or sentry
            return None

        if file_type == 'xml':
            doc = Et.parse("%s%s" % (files_folder, file_name))
            return XmlRoutesParser().load_routes(doc)
        elif file_type == 'json':
            raise NotImplementedError

        return None

    @abstractmethod
    def load_routes(self, file_name: str):
        raise NotImplementedError


# noinspection PyMethodMayBeStatic
class XmlRoutesParser(RoutesParser):
    """
    Загрузим маршруты из xml файла поставщиков
    """

    def load_routes(self, xml_doc) -> list:
        """
        Из xml документа загрузим маршруты, состоящие из цен и перелетов
        :param xml_doc:
        :return:
        """
        routes = []

        for xml_routes in xml_doc.find('PricedItineraries'):
            prices: list = self.get_prices(xml_routes.find('Pricing'))

            if prices:
                for xml_path in ['OnwardPricedItinerary/Flights', 'ReturnPricedItinerary/Flights']:
                    flight = self.get_route(xml_routes.find(xml_path)) if xml_routes.find(
                        xml_path) else None
                    if flight:
                        flight.prices = prices
                        routes.append(flight)

        return routes

    def get_route(self, xml_obj) -> Route:
        """
        Распарсим xml и получим маршрут
        :param xml_obj:
        :return:
        """

        try:
            route = Route()
            for part_of_flight in xml_obj:
                flight_attrs = {
                    attr.tag: str(attr.text) if attr.text else '' for attr in part_of_flight
                }
                flight_attrs['CarrierId'] = part_of_flight.find('Carrier').attrib.get("id")
                route.flights = FlightPartSchema().load(flight_attrs)

            return route
        except Exception as err:
            print('err - %s' % err)
            # TODO log error, sentry
            return []

    def get_prices(self, xml_obj) -> list:
        """
        Распарсим xml и получим цены. Каждый пассажир - это одна цена, поэтому отдаем список цен
        :param xml_obj:
        :return:
        """

        result: list = []
        service_charges: dict = defaultdict(dict)
        currency: str = xml_obj.attrib.get('currency', None)

        for service_charge in xml_obj:
            passenger: str = service_charge.attrib.get('type')
            service_charges[passenger].update({service_charge.attrib.get('ChargeType'): float(service_charge.text)})

        for passenger, service_charge in service_charges.items():
            service_charge.update({passenger: True, 'currency': currency})
            result.append(service_charge)

        try:
            return FlightPriceSchema(many=True).load(result)
        except Exception as er:
            return []


class JsonRoutesParser(RoutesParser):
    """
    Загрузим маршруты из json файла поставщиков
    """

    def load_routes(self, json_doc):
        raise NotImplementedError
