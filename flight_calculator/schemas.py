from marshmallow import Schema, fields, post_load


# ############################################ FlightPrice ###########################################################

class FlightPriceSchema(Schema):
    base_price: float = fields.Float(required=True, data_key='BaseFare')
    taxes: float = fields.Float(data_key='AirlineTaxes')
    total_price: float = fields.Float(required=True, data_key='TotalAmount')
    currency: str = fields.Str(required=True)
    adult: bool = fields.Bool(data_key='SingleAdult')
    child: bool = fields.Bool(data_key='SingleChild')
    infant: bool = fields.Bool(data_key='SingleInfant')

    @post_load
    def create(self, data):
        return FlightPrice(**data)


class FlightPrice(object):
    """
    Объект содержащий информацию о цене перелета для опредленного вида пассажира
    """

    def __init__(self, base_price: float, taxes: float, total_price: float, currency: str, adult=False, child=False,
                 infant=False):
        """
        :param base_price: Базовая цена на билет
        :param taxes: Коммисия Авиакомпании
        :param total_price: Итоговая цена
        :param currency: валюта
        :param adult: Тип пассажира
        :param child: Тип пассажира
        :param infant: Тип пассажира
        """
        self.base_price: float = base_price
        self.taxes: float = taxes
        self.total_price: float = total_price
        self.currency: str = currency
        self.adult: bool = adult
        self.child: bool = child
        self.infant: bool = infant

    @property
    def passenger(self):
        if self.child:
            return 'child'
        elif self.infant:
            return 'infant'

        return 'adult'


# ############################################ FlightPart ###########################################################

class FlightPartSchema(Schema):
    carrier_id: str = fields.String(required=True, data_key='CarrierId')
    carrier: str = fields.String(required=True, data_key='Carrier')
    flight_number: str = fields.String(required=True, data_key='FlightNumber')
    source: str = fields.String(required=True, data_key='Source')
    destination: str = fields.String(required=True, data_key='Destination')
    departure_datetime = fields.DateTime(required=True, data_key='DepartureTimeStamp', format='%Y-%m-%dT%H%M')
    arrival_datetime = fields.DateTime(required=True, data_key='ArrivalTimeStamp', format='%Y-%m-%dT%H%M')
    fare_basis: str = fields.String(required=True, data_key='FareBasis')
    flight_class: str = fields.String(data_key='Class')
    stops_number: int = fields.Int(data_key='NumberOfStops')
    warning_text: str = fields.String(data_key='WarningText')
    ticket_type: str = fields.String(data_key='TicketType')

    @post_load
    def create(self, data):
        return FlightPart(**data)


class FlightPart(object):
    """
        Объект содержащий информацию о перелете
    """

    def __init__(self, carrier_id, carrier, flight_number, source, destination, departure_datetime, arrival_datetime,
                 fare_basis, flight_class, stops_number, warning_text, ticket_type):
        """
        :param carrier_id:
        :param carrier:
        :param flight_number:
        :param source:
        :param destination:
        :param departure_datetime:
        :param arrival_datetime:
        :param fare_basis:
        :param flight_class:
        :param stops_number:
        :param warning_text:
        :param ticket_type:
        """
        fare_basis = fare_basis.replace('\n', '').replace(' ', '')

        self.carrier_id = carrier_id
        self.carrier = carrier
        self.flight_number = flight_number
        self.source = source
        self.destination = destination
        self.departure_datetime = departure_datetime
        self.arrival_datetime = arrival_datetime
        self.fare_basis = fare_basis
        self.flight_class = flight_class
        self.stops_number = stops_number
        self.warning_text = warning_text
        self.ticket_type = ticket_type


# ############################################ Flight #################################################################

class RouteSchema(Schema):
    flights: list = fields.List(fields.Nested(FlightPartSchema), many=True)
    prices: list = fields.List(fields.Nested(FlightPriceSchema), many=True)

    @post_load
    def create(self, data):
        return Route(**data)


class Route(object):
    """
        Маршрут - это объект, состоящий из цены и перелета(ов)
    """

    def __init__(self, flights: list = None, prices: list = None):
        self._flights: list = flights if flights else []
        self._prices: list = prices if prices else []

    @property
    def flights(self):
        return self._flights

    @flights.setter
    def flights(self, v: list):
        self._flights.append(v)

    @property
    def prices(self):
        return self._prices

    @prices.setter
    def prices(self, v: list):
        self._prices = v

    @property
    def source(self):
        return self.flights[0].source

    @property
    def destination(self):
        return self.flights[-1].destination

    @property
    def departure_datetime(self):
        return self.flights[0].departure_datetime

    @property
    def arrival_datetime(self):
        return self.flights[-1].arrival_datetime

    @property
    def flight_number(self):
        return [f_p.flight_number for f_p in self.flights]

    @property
    def carrier(self):
        return [f_p.carrier for f_p in self.flights]

    @property
    def stops_number(self):
        count = len(self.flights) - 1
        for f_p in self.flights:
            count = count + f_p.stops_number

        return count

    @property
    def adult_price(self):
        price = list(filter(lambda p: p.passenger == 'adult', self._prices))
        return price[0] if price else None

    @property
    def child_price(self):
        price = list(filter(lambda p: p.passenger == 'child', self._prices))
        return price[0] if price else None

    @property
    def infant_price(self):
        price = list(filter(lambda p: p.passenger == 'infant', self._prices))
        return price[0] if price else None

    @property
    def travel_time(self):
        return int((self.arrival_datetime - self.departure_datetime).total_seconds())


# ############################################ RoutesList ##############################################################

class RoutesListSchema(Schema):
    routes: list = fields.List(fields.Nested(RouteSchema), many=True)

    @post_load
    def create(self, data):
        return RoutesList(**data)


class RoutesList(object):
    """
    Список маршрутов
    """

    def __init__(self, routes: list = None):
        self._routes: list = routes if routes else []

    @property
    def routes(self):
        return self._routes

    @routes.setter
    def routes(self, v):
        self._routes.append(v)

    def sort(self, order_field: str, order_value: str = 'asc', limit: int = 10):
        """
        Отсортируем полеты
        :param order_field: 
        :param order_value: 
        :param limit: 
        :return: 
        """

        # TODO добавить фильтр по passenger
        assert order_field in ('price', 'time', 'optimal')
        assert order_value in ('asc', 'desc')

        if order_field == 'price':
            key = lambda f: f.adult_price.total_price
        elif order_field == 'time':
            key = lambda f: f.travel_time
        elif order_field == 'optimal':
            key = lambda f: (f.adult_price.total_price, f.travel_time)
        else:
            key = None

        self._routes = sorted(self._routes, key=key, reverse=True if order_value == 'desc' else False)[:limit]
