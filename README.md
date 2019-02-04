Вебсервис, отвечающий на два вопроса:
* Какие варианты перелёта из DXB в BKK мы получили?
* Самый дорогой/дешёвый, быстрый/долгий и оптимальный варианты

К сожалению я поздно понял суть 3-го вопроса:
В чём отличия между результатами двух запросов (изменение маршрутов/условий)?

Т.к я думал что два xml файла это разные данные от разных поставщиков данных, поэтому с текущим подходом ответить не него не получилось.
Само приложение парсит маршруты из xml файлов и создает объекты с перелетами и ценами, валидирует их и возвращает.

Для запуска приложения:
1. надо создать базовый образ `docker build -t aviasales-test/base/python base/python`
2. запустить сам микросервис `docker-compose up -d`
3. Для запуска тестов `docker-compose exec flight_calculator runtests`


API:
http://localhost/get_routes?source=DXB&destination=BKK&departure_date=2018-10-27

Самый дорогой\дешевый т.д. было сделано через фильтрацию этого же запроса.
* http://localhost/get_routes?source=DXB&destination=BKK&departure_date=2018-10-27&order_field=price&order_value=asc&limit=1
* http://localhost/get_routes?source=DXB&destination=BKK&departure_date=2018-10-27&order_field=price&order_value=desc&limit=1

* http://localhost/get_routes?source=DXB&destination=BKK&departure_date=2018-10-27&order_field=time&order_value=desc&limit=1
* http://localhost/get_routes?source=DXB&destination=BKK&departure_date=2018-10-27&order_field=time&order_value=desc&limit=1

* http://localhost/get_routes?source=DXB&destination=BKK&departure_date=2018-10-27&order_field=optimal&order_value=desc&limit=1
* http://localhost/get_routes?source=DXB&destination=BKK&departure_date=2018-10-27&order_field=optimal&order_value=desc&limit=1
