import requests
import json


def test(code):
    url = f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/stopArrivalTimes?stopId={code}'  # Замените на URL вашего XML-файла
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()  # Получаем данные JSON
        # Проверяем наличие ключа 'ArrivalTime' и выводим его значение
        if 'ArrivalTime' in json_data:
            arrival_times = json_data['ArrivalTime']
            num_arrival_times = len(arrival_times)  # Находим длину arrival_times
            if num_arrival_times:
                for arrival_time in arrival_times:
                    route_number = arrival_time['RouteNumber']
                    minutes = arrival_time['ArrivalTime']
                    print(f"Автобус {route_number} прибудет через {minutes} минут")
            else:
                print(f"В данный момент отсутсвует маршруты автобусов")
        else:
            print('Ключ ArrivalTime не найден в данных JSON')
    else:
        print('Ошибка при выполнении запроса:', response.status_code)


if __name__ == '__main__':
    # Отправка запроса к веб-сайту
    code_bus_stop = 1740
    print(f"Время автобусом на остановке ID:{code_bus_stop}")
    test(code_bus_stop)