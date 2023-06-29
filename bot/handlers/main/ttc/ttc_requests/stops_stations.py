import httpx
from transliterate import translit


async def fetch_stops_data():
    url = "http://transfer.ttc.com.ge:8080/otp/routers/ttc/index/stops"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    resp.raise_for_status()  # выбрасывает исключение, если запрос завершился неудачей
    data = resp.json()

    # Отделяем остановки от станций
    stops = [item for item in data if 'code' in item and item['code'].isdigit()]
    stations = [item for item in data if item not in stops]

    # Добавляем транслитерацию
    for stop in stops:
        stop['name_translit'] = translit(stop['name'], 'ka', reversed=True)

    for station in stations:
        station['name_translit'] = translit(station['name'], 'ka', reversed=True)

    # Сортируем и сохраняем данные в разные файлы
    stops.sort(key=lambda item: int(item['code']))
    stations.sort(key=lambda item: str(item['id'].split(":")[1]))

    return [stops, stations]
