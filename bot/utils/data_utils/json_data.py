import json


# Функция для сохранения данных в JSON-файле
async def save_json_data(name_file: str, json_data):
    with open(f'./data/json/{name_file}.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


async def load_json_data(name_file: str, tag: str = None):
    with open(f'./data/json/{name_file}.json', 'r') as f:
        stops_data = json.load(f)
    if tag is None:
        return stops_data
    else:
        return {stop[tag] for stop in stops_data}
