import json


# Функция для сохранения данных остановок в JSON-файле
def save_stops_data(stops_data):
    with open('./data/stops_data.json', 'w', encoding='utf-8') as f:
        json.dump(stops_data, f, ensure_ascii=False, indent=4)


def load_stops_data(tag: str = None):
    with open('./data/stops_data.json', 'r') as f:
        stops_data = json.load(f)
    if tag is None:
        return stops_data
    else:
        return {stop[tag] for stop in stops_data}

# Функция для сохранения данных станций в JSON-файле
def save_stations_data(stations_data):
    with open('./data/stations_data.json', 'w', encoding='utf-8') as f:
        json.dump(stations_data, f, ensure_ascii=False, indent=4)


def load_stations_data():
    with open('./data/stations_data.json', 'r') as f:
        stations_data = json.load(f)
    return stations_data
