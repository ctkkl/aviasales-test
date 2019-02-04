import unittest
from datetime import datetime, date
from models import RoutesHandler
import xml.etree.ElementTree as Et
from parser import XmlRoutesParser
from schemas import FlightPrice, RoutesList, Route

partner_doc = '''
<AirFareSearchResponse RequestTime="28-09-2015 20:23:49" ResponseTime="28-09-2015 20:23:56">
    <RequestId>123ABCD</RequestId>
    <PricedItineraries>
        <Flights>
            <OnwardPricedItinerary>
                <Flights>
                    <Flight>
                        <Carrier id="AI">AirIndia</Carrier>
                        <FlightNumber>996</FlightNumber>
                        <Source>DXB</Source>
                        <Destination>DEL</Destination>
                        <DepartureTimeStamp>2018-10-22T0005</DepartureTimeStamp>
                        <ArrivalTimeStamp>2018-10-22T0445</ArrivalTimeStamp>
                        <Class>G</Class>
                        <NumberOfStops>0</NumberOfStops>
                        <FareBasis>
                            2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_DEL_996_9_00:05_$255_DEL_BKK_332_9_13:50_$255_BKK_DEL_333_9_08:50_$255_DEL_DXB_995_9_20:40__A2_0_0
                        </FareBasis>
                        <WarningText/>
                        <TicketType>E</TicketType>
                    </Flight>
                    <Flight>
                        <Carrier id="AI">AirIndia</Carrier>
                        <FlightNumber>332</FlightNumber>
                        <Source>DEL</Source>
                        <Destination>BKK</Destination>
                        <DepartureTimeStamp>2018-10-22T1350</DepartureTimeStamp>
                        <ArrivalTimeStamp>2018-10-22T1935</ArrivalTimeStamp>
                        <Class>G</Class>
                        <NumberOfStops>0</NumberOfStops>
                        <FareBasis>
                            2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_DEL_996_9_00:05_$255_DEL_BKK_332_9_13:50_$255_BKK_DEL_333_9_08:50_$255_DEL_DXB_995_9_20:40__A2_0_0
                        </FareBasis>
                        <WarningText/>
                        <TicketType>E</TicketType>
                    </Flight>
                </Flights>
            </OnwardPricedItinerary>
            <ReturnPricedItinerary>
                <Flights>
                    <Flight>
                        <Carrier id="AI">AirIndia</Carrier>
                        <FlightNumber>333</FlightNumber>
                        <Source>BKK</Source>
                        <Destination>DEL</Destination>
                        <DepartureTimeStamp>2018-10-30T0850</DepartureTimeStamp>
                        <ArrivalTimeStamp>2018-10-30T1205</ArrivalTimeStamp>
                        <Class>U</Class>
                        <NumberOfStops>0</NumberOfStops>
                        <FareBasis>
                            2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_DEL_996_9_00:05_$255_DEL_BKK_332_9_13:50_$255_BKK_DEL_333_9_08:50_$255_DEL_DXB_995_9_20:40__A2_0_0
                        </FareBasis>
                        <WarningText/>
                        <TicketType>E</TicketType>
                    </Flight>
                    <Flight>
                        <Carrier id="AI">AirIndia</Carrier>
                        <FlightNumber>995</FlightNumber>
                        <Source>DEL</Source>
                        <Destination>DXB</Destination>
                        <DepartureTimeStamp>2018-10-30T2040</DepartureTimeStamp>
                        <ArrivalTimeStamp>2018-10-30T2245</ArrivalTimeStamp>
                        <Class>U</Class>
                        <NumberOfStops>0</NumberOfStops>
                        <FareBasis>
                            2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_DEL_996_9_00:05_$255_DEL_BKK_332_9_13:50_$255_BKK_DEL_333_9_08:50_$255_DEL_DXB_995_9_20:40__A2_0_0
                        </FareBasis>
                        <WarningText/>
                        <TicketType>E</TicketType>
                    </Flight>
                </Flights>
            </ReturnPricedItinerary>
            <Pricing currency="SGD">
                <ServiceCharges type="SingleAdult" ChargeType="BaseFare">117.00</ServiceCharges>
                <ServiceCharges type="SingleAdult" ChargeType="AirlineTaxes">429.80</ServiceCharges>
                <ServiceCharges type="SingleAdult" ChargeType="TotalAmount">546.80</ServiceCharges>
            </Pricing>
        </Flights>
        <Flights>
            <OnwardPricedItinerary>
                <Flights>
                    <Flight>
                        <Carrier id="MH">Malaysia Airlines</Carrier>
                        <FlightNumber>163</FlightNumber>
                        <Source>DXB</Source>
                        <Destination>KUL</Destination>
                        <DepartureTimeStamp>2018-10-22T1935</DepartureTimeStamp>
                        <ArrivalTimeStamp>2018-10-23T0705</ArrivalTimeStamp>
                        <Class>N</Class>
                        <NumberOfStops>0</NumberOfStops>
                        <FareBasis>
                            2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_KUL_163_44_19:35_$255_KUL_BKK_5860_44_13:20_$255_BKK_KUL_785_44_11:05_$255_KUL_DXB_162_44_15:15__A2_0_0
                        </FareBasis>
                        <WarningText/>
                        <TicketType>E</TicketType>
                    </Flight>
                    <Flight>
                        <Carrier id="MH">Malaysia Airlines</Carrier>
                        <FlightNumber>5860</FlightNumber>
                        <Source>KUL</Source>
                        <Destination>BKK</Destination>
                        <DepartureTimeStamp>2018-10-23T1320</DepartureTimeStamp>
                        <ArrivalTimeStamp>2018-10-23T1430</ArrivalTimeStamp>
                        <Class>L</Class>
                        <NumberOfStops>0</NumberOfStops>
                        <FareBasis>
                            2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_KUL_163_44_19:35_$255_KUL_BKK_5860_44_13:20_$255_BKK_KUL_785_44_11:05_$255_KUL_DXB_162_44_15:15__A2_0_0
                        </FareBasis>
                        <WarningText/>
                        <TicketType>E</TicketType>
                    </Flight>
                </Flights>
            </OnwardPricedItinerary>
            <ReturnPricedItinerary>
                <Flights>
                    <Flight>
                        <Carrier id="MH">Malaysia Airlines</Carrier>
                        <FlightNumber>785</FlightNumber>
                        <Source>BKK</Source>
                        <Destination>KUL</Destination>
                        <DepartureTimeStamp>2018-10-30T1105</DepartureTimeStamp>
                        <ArrivalTimeStamp>2018-10-30T1415</ArrivalTimeStamp>
                        <Class>N</Class>
                        <NumberOfStops>0</NumberOfStops>
                        <FareBasis>
                            2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_KUL_163_44_19:35_$255_KUL_BKK_5860_44_13:20_$255_BKK_KUL_785_44_11:05_$255_KUL_DXB_162_44_15:15__A2_0_0
                        </FareBasis>
                        <WarningText/>
                        <TicketType>E</TicketType>
                    </Flight>
                    <Flight>
                        <Carrier id="MH">Malaysia Airlines</Carrier>
                        <FlightNumber>162</FlightNumber>
                        <Source>KUL</Source>
                        <Destination>DXB</Destination>
                        <DepartureTimeStamp>2018-10-30T1515</DepartureTimeStamp>
                        <ArrivalTimeStamp>2018-10-30T1850</ArrivalTimeStamp>
                        <Class>N</Class>
                        <NumberOfStops>0</NumberOfStops>
                        <FareBasis>
                            2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_KUL_163_44_19:35_$255_KUL_BKK_5860_44_13:20_$255_BKK_KUL_785_44_11:05_$255_KUL_DXB_162_44_15:15__A2_0_0
                        </FareBasis>
                        <WarningText/>
                        <TicketType>E</TicketType>
                    </Flight>
                </Flights>
            </ReturnPricedItinerary>
            <Pricing currency="SGD">
                <ServiceCharges type="SingleAdult" ChargeType="BaseFare">563.00</ServiceCharges>
                <ServiceCharges type="SingleAdult" ChargeType="AirlineTaxes">60.80</ServiceCharges>
                <ServiceCharges type="SingleAdult" ChargeType="TotalAmount">623.80</ServiceCharges>
            </Pricing>
        </Flights>
    </PricedItineraries>
</AirFareSearchResponse>
    '''


def get_routes_from_files_mock():
    return list(XmlRoutesParser().load_routes(Et.fromstring(partner_doc)))


class XmlModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_xml_get_prices_for_adult(self):
        """
        Получим цены на перелет из xml для взрослого
        :return:
        """
        xml_price = Et.fromstring('''
        <Pricing currency="SGD">
            <ServiceCharges type="SingleAdult" ChargeType="BaseFare">800.00</ServiceCharges>
            <ServiceCharges type="SingleAdult" ChargeType="AirlineTaxes">579.80</ServiceCharges>
            <ServiceCharges type="SingleAdult" ChargeType="TotalAmount">1379.80</ServiceCharges>
        </Pricing>
        ''')
        prices = XmlRoutesParser().get_prices(xml_price)

        self.assertEqual(1, len(prices))
        self.assertIsInstance(prices[0], (FlightPrice,))

        # check mapping
        self.assertEqual(800.00, prices[0].base_price)
        self.assertEqual(579.80, prices[0].taxes)
        self.assertEqual(1379.80, prices[0].total_price)
        self.assertEqual('SGD', prices[0].currency)
        self.assertEqual(True, prices[0].adult)
        self.assertEqual(False, prices[0].child)
        self.assertEqual(False, prices[0].infant)

    def test_xml_get_prices_for_adult_child_infant(self):
        """
        Получим цены на перелет из xml для взрослого
        :return:
        """
        xml_price = Et.fromstring('''
        <Pricing currency="SGD">
            <ServiceCharges type="SingleAdult" ChargeType="BaseFare">4544.00</ServiceCharges>
            <ServiceCharges type="SingleAdult" ChargeType="AirlineTaxes">348.10</ServiceCharges>
            <ServiceCharges type="SingleAdult" ChargeType="TotalAmount">4892.10</ServiceCharges>
            <ServiceCharges type="SingleChild" ChargeType="BaseFare">3410.00</ServiceCharges>
            <ServiceCharges type="SingleChild" ChargeType="AirlineTaxes">348.10</ServiceCharges>
            <ServiceCharges type="SingleChild" ChargeType="TotalAmount">3758.10</ServiceCharges>
            <ServiceCharges type="SingleInfant" ChargeType="BaseFare">455.00</ServiceCharges>
            <ServiceCharges type="SingleInfant" ChargeType="AirlineTaxes">7.20</ServiceCharges>
            <ServiceCharges type="SingleInfant" ChargeType="TotalAmount">462.20</ServiceCharges>
        </Pricing>
        ''')
        prices = XmlRoutesParser().get_prices(xml_price)

        self.assertEqual(3, len(prices))

        # check mapping
        self.assertEqual(4544.00, prices[0].base_price)
        self.assertEqual(348.10, prices[0].taxes)
        self.assertEqual(4892.10, prices[0].total_price)
        self.assertEqual('SGD', prices[0].currency)
        self.assertEqual(True, prices[0].adult)
        self.assertEqual(False, prices[0].child)
        self.assertEqual(False, prices[0].infant)

        self.assertEqual(3410.00, prices[1].base_price)
        self.assertEqual(348.10, prices[1].taxes)
        self.assertEqual(3758.10, prices[1].total_price)
        self.assertEqual('SGD', prices[1].currency)
        self.assertEqual(False, prices[1].adult)
        self.assertEqual(True, prices[1].child)
        self.assertEqual(False, prices[1].infant)

        self.assertEqual(455.00, prices[2].base_price)
        self.assertEqual(7.20, prices[2].taxes)
        self.assertEqual(462.20, prices[2].total_price)
        self.assertEqual('SGD', prices[2].currency)
        self.assertEqual(False, prices[2].adult)
        self.assertEqual(False, prices[2].child)
        self.assertEqual(True, prices[2].infant)

    def test_xml_get_prices_error(self):
        """
        Передадим плохой xml
        :return:
        """
        xml_price = Et.fromstring('''
        <Pricing currency="SGD">
        </Pricing>
        ''')
        self.assertEqual([], XmlRoutesParser().get_prices(xml_price))

        xml_price = Et.fromstring('''
        <Pricing currency="SGD">
            <ServiceCharges type="SingleOldMan" ChargeType="BaseFare">4544.00</ServiceCharges>
        </Pricing>
        ''')
        self.assertEqual([], XmlRoutesParser().get_prices(xml_price))

    def test_get_routes_from_1_part(self):
        """
        Получим полет, состоящий их 1-ой части
        :return:
        """
        xml_data = Et.fromstring('''
        <Flights>
            <Flight>
                <Carrier id="QF">Qantas</Carrier>
                <FlightNumber>8354</FlightNumber>
                <Source>DXB</Source>
                <Destination>SIN</Destination>
                <DepartureTimeStamp>2018-10-27T0315</DepartureTimeStamp>
                <ArrivalTimeStamp>2018-10-27T1440</ArrivalTimeStamp>
                <Class>S</Class>
                <NumberOfStops>0</NumberOfStops>
                <FareBasis>
2820303decf751-5511-447a-aeb1-810a6b10ad7d@@$255_DXB_SIN_8354_48_03:15_$255_SIN_BKK_978_52_18:45__A2_1_1
</FareBasis>
                <WarningText/>
                <TicketType>E</TicketType>
            </Flight>
        </Flights>
        ''')

        route = XmlRoutesParser().get_route(xml_data)
        routes_list = route.flights
        self.assertEqual(1, len(routes_list))

        # check mapping
        self.assertEqual('QF', routes_list[0].carrier_id)
        self.assertEqual('Qantas', routes_list[0].carrier)
        self.assertEqual('8354', routes_list[0].flight_number)
        self.assertEqual('DXB', routes_list[0].source)
        self.assertEqual('SIN', routes_list[0].destination)
        self.assertEqual(datetime(2018, 10, 27, 3, 15), routes_list[0].departure_datetime)
        self.assertEqual(datetime(2018, 10, 27, 14, 40), routes_list[0].arrival_datetime)
        self.assertEqual('2820303decf751-5511-447a-aeb1-810a6b10ad7d@@$255_DXB_SIN_8354_48_03:15_$255_'
                         'SIN_BKK_978_52_18:45__A2_1_1', routes_list[0].fare_basis)
        self.assertEqual('S', routes_list[0].flight_class)
        self.assertEqual(0, routes_list[0].stops_number)
        self.assertEqual('', routes_list[0].warning_text)
        self.assertEqual('E', routes_list[0].ticket_type)

        # проверим что source\destination высчитается из двух частей
        self.assertEqual('DXB', route.source)
        self.assertEqual('SIN', route.destination)

    def test_get_routes_from_2_parts(self):
        """
        Получим полет, состоящий их 2-ух частей
        :return:
        """
        xml_data = Et.fromstring('''
        <Flights>
            <Flight>
                <Carrier id="QF">Qantas</Carrier>
                <FlightNumber>8354</FlightNumber>
                <Source>DXB</Source>
                <Destination>SIN</Destination>
                <DepartureTimeStamp>2018-10-27T0315</DepartureTimeStamp>
                <ArrivalTimeStamp>2018-10-27T1440</ArrivalTimeStamp>
                <Class>S</Class>
                <NumberOfStops>0</NumberOfStops>
                <FareBasis>
2820303decf751-5511-447a-aeb1-810a6b10ad7d@@$255_DXB_SIN_8354_48_03:15_$255_SIN_BKK_978_52_18:45__A2_1_1
</FareBasis>
                <WarningText/>
                <TicketType>E</TicketType>
            </Flight>
            <Flight>
                <Carrier id="SQ">Singapore Airlines</Carrier>
                <FlightNumber>978</FlightNumber>
                <Source>SIN</Source>
                <Destination>BKK</Destination>
                <DepartureTimeStamp>2018-10-27T1845</DepartureTimeStamp>
                <ArrivalTimeStamp>2018-10-27T2010</ArrivalTimeStamp>
                <Class>B</Class>
                <NumberOfStops>0</NumberOfStops>
                <FareBasis>
2820303decf751-5511-447a-aeb1-810a6b10ad7d@@$255_DXB_SIN_8354_48_03:15_$255_SIN_BKK_978_52_18:45__A2_1_1
</FareBasis>
                <WarningText/>
                <TicketType>E</TicketType>
            </Flight>
        </Flights>
        ''')

        route = XmlRoutesParser().get_route(xml_data)
        routes_list = route.flights
        self.assertEqual(2, len(routes_list))

        # check mapping
        self.assertEqual('QF', routes_list[0].carrier_id)
        self.assertEqual('Qantas', routes_list[0].carrier)
        self.assertEqual('8354', routes_list[0].flight_number)
        self.assertEqual('DXB', routes_list[0].source)
        self.assertEqual('SIN', routes_list[0].destination)
        self.assertEqual(datetime(2018, 10, 27, 3, 15), routes_list[0].departure_datetime)
        self.assertEqual(datetime(2018, 10, 27, 14, 40), routes_list[0].arrival_datetime)
        self.assertEqual('2820303decf751-5511-447a-aeb1-810a6b10ad7d@@$255_DXB_SIN_8354_48_03:15_$255_'
                         'SIN_BKK_978_52_18:45__A2_1_1', routes_list[0].fare_basis)
        self.assertEqual('S', routes_list[0].flight_class)
        self.assertEqual(0, routes_list[0].stops_number)
        self.assertEqual('', routes_list[0].warning_text)
        self.assertEqual('E', routes_list[0].ticket_type)

        # проверим что source\destination высчитается из двух частей
        self.assertEqual('DXB', route.source)
        self.assertEqual('BKK', route.destination)

    def test_get_routes(self):
        """
        Полная проверка на получение полетов в модели
        :return:
        """
        xml_data = Et.fromstring(partner_doc)

        routes = list(XmlRoutesParser().load_routes(xml_data))
        self.assertEqual(4, len(routes))

    def test_calculate_on_mock(self):
        """
        Получим полеты с определенными условиями, на мок данных
        :return:
        """

        # mock data
        calc = RoutesHandler()
        calc.get_routes_call = get_routes_from_files_mock

        routes_list = calc.calculate(source='DXB', destination='BKK', departure_date=date(2018, 10, 22))
        self.assertIsInstance(routes_list, (RoutesList,))
        self.assertEqual(2, len(routes_list.routes))

        self.assertEqual(['996', '332'], routes_list.routes[0].flight_number)
        self.assertEqual(['163', '5860'], routes_list.routes[1].flight_number)

        routes_list = calc.calculate(source='BKK', destination='DXB', departure_date=date(2018, 10, 22))
        self.assertEqual(0, len(routes_list.routes))

        routes_list = calc.calculate(source='BKK', destination='DXB', departure_date=date(2018, 10, 30))
        self.assertEqual(2, len(routes_list.routes))

        self.assertEqual(['333', '995'], routes_list.routes[0].flight_number)
        self.assertEqual(['785', '162'], routes_list.routes[1].flight_number)

    def test_filter_on_mock(self):
        """
        Отфильтруем полеты, на мок данных
        :return:
        """
        # mock data
        calc = RoutesHandler()
        calc.get_routes_call = get_routes_from_files_mock

        routes_list = calc.calculate(source='DXB', destination='BKK', departure_date=date(2018, 10, 22))
        self.assertEqual(2, len(routes_list.routes))

        routes_list.sort('price', order_value='asc')
        self.assertEqual(546.8, routes_list.routes[0].adult_price.total_price)
        self.assertEqual(623.8, routes_list.routes[1].adult_price.total_price)

        routes_list.sort('price', order_value='desc')
        self.assertEqual(623.8, routes_list.routes[0].adult_price.total_price)
        self.assertEqual(546.8, routes_list.routes[1].adult_price.total_price)

    def test_calculate_and_filter_on_real_date(self):
        """
        Проверим работу сортировки на реальных данных из файлов
        :return:
        """

        routes_list = RoutesHandler().calculate(source='DXB', destination='BKK', departure_date=date(2018, 10, 27))
        self.assertEqual(102, len(routes_list.routes))

        # sort by price

        routes_list.sort('price', order_value='asc', limit=100)
        prev_value = None
        for flight in routes_list.routes:
            current_value = flight.adult_price.total_price
            if prev_value:
                self.assertEqual(True, current_value >= prev_value)

            prev_value = current_value

        routes_list.sort('price', order_value='desc', limit=100)
        self.assertEqual(100, len(routes_list.routes))
        prev_value = None
        for flight in routes_list.routes:
            current_value = flight.adult_price.total_price
            if prev_value:
                self.assertEqual(True, current_value <= prev_value)

            prev_value = current_value

        # sort by time

        routes_list.sort('time', order_value='asc', limit=100)
        prev_value = None
        for flight in routes_list.routes:
            current_value = flight.travel_time
            if prev_value:
                self.assertEqual(True, current_value >= prev_value)

            prev_value = current_value

        routes_list.sort('time', order_value='desc')
        prev_value = None
        for flight in routes_list.routes:
            current_value = flight.travel_time
            if prev_value:
                self.assertEqual(True, current_value <= prev_value)

            prev_value = current_value

        # optimal
        routes_list.sort('optimal', order_value='asc')
        prev_price, prev_time = None, None
        for flight in routes_list.routes:
            current_price, current_time = flight.adult_price.total_price, flight.travel_time
            if prev_price:
                self.assertEqual(True, current_price >= prev_price)
                if prev_price == current_price:
                    self.assertEqual(True, current_time >= prev_time)

            prev_price, prev_time = current_price, current_time
