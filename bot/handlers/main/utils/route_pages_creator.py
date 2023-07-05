import os
import folium
import folium.plugins

from bot.utils.additional import number_to_emoji
from bot.utils.data_utils.json_data import load_json_data
from data import config


class PageBuilder:
    def __init__(self, route_number: str):
        self.route_number = route_number

    async def check_forwards(self) -> list:
        have_forwards = []
        for forward in [0, 1]:
            data = await load_json_data(f"routes/{self.route_number}_forward_{forward}")

            shape = data['Shape']
            if shape != '':
                have_forwards.append(forward)
        return have_forwards

    async def get_route_directions(self, forwards, language) -> list:
        route_directions = []
        for index, forward in enumerate(forwards):
            data = await load_json_data(f"routes/{self.route_number}_forward_{forward}")

            # Извлечение данных о остановках
            stops = data['RouteStops']
            name = 'Name' if language == 'ka' else 'Name_translit'
            # Получение имени первой и последней остановки
            first_stop_name = stops[0][name]
            last_stop_name = stops[-1][name]
            route_directions.append(f"{number_to_emoji(index)} {first_stop_name} 👉 {last_stop_name}")
        return route_directions

    async def __get_coord_info(self, forward: str):

        data = await load_json_data(f"routes/{self.route_number}_forward_{forward}")

        shape = data['Shape']

        coordinates = shape.split(",")
        coordinates = [(float(c.split(":")[1]), float(c.split(":")[0])) for c in coordinates]

        stops = data['RouteStops']
        stop_info = [(float(stop['Lat']), float(stop['Lon']), stop['StopId']) for stop in stops]

        return coordinates, stop_info

    async def create_page(self, forward: str) -> str:
        existing_files = os.path.exists(f'home_page/routes/{self.route_number}_forward_{forward}.html')
        if existing_files and not config.REFRESH_BUS_ROUTES:
            # If file already exists, just send the first match
            html_name = f'{self.route_number}_forward_{forward}.html'
        else:
            # Fetch the route data and generate the map
            coordinates, stop_info = await self.__get_coord_info(forward)
            # Make map with folium
            m = folium.Map(location=coordinates[0], zoom_start=14)

            m.get_root().html.add_child(folium.JavascriptLink('https://telegram.org/js/telegram-web-app.js'))

            # # Загружаем и читаем JavaScript файл
            # with open('./data/static/js/route_page.js', 'r') as f:
            #     js = f.read()
            # # Оборачиваем содержимое файла в теги <script>
            # js = '<script type="text/javascript">' + js + '</script>'
            #
            # js_element = folium.Element(js)
            #
            # # Добавляем этот элемент на карту
            # m.get_root().html.add_child(js_element)

            m.get_root().html.add_child(folium.JavascriptLink("./data/static/js/route_page.js"))
            folium.plugins.AntPath(coordinates, color="#3d00f7", delay=1000, weight=2.5, opacity=1).add_to(m)

            for stop in stop_info:
                icon = folium.features.CustomIcon('./data/static/media/bus_stop_icon.png',
                                                  icon_size=[18, 18])  # Add custom icon
                folium.Marker(location=(stop[0], stop[1]),
                              popup=f"Stop ID: <b>{stop[2]}</b>",
                              icon=icon).add_to(m)
            m.fit_bounds(coordinates)  # Automatically adjust map to show the whole route
            html_name = f'{self.route_number}_forward_{forward}.html'

            m.save(os.path.join('home_page', 'routes', html_name))

        return html_name
