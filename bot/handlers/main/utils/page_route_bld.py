import os
import folium
import folium.plugins

from bot.handlers.main.utils.folium_web_app_bld import FoliumWebAppBuilder
from bot.utils.additional import number_to_emoji
from bot.utils.data_utils.json_data import load_json_data
from bot.utils.localization.i18n import MessageFormatter
from data import config


class PageRouteBuilder:
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
        for forward in forwards:
            data = await load_json_data(f"routes/{self.route_number}_forward_{forward}")

            # Извлечение данных о остановках
            stops = data['RouteStops']
            name = 'Name' if language == 'ka' else 'Name_translit'
            # Получение имени первой и последней остановки
            first_stop_name = stops[0][name]
            last_stop_name = stops[-1][name]
            route_directions.append(f"{number_to_emoji(forward)} {first_stop_name} 👉 {last_stop_name}")
        return route_directions

    async def __get_coord_info(self, forward: str):

        data = await load_json_data(f"routes/{self.route_number}_forward_{forward}")

        shape = data['Shape']

        coordinates = shape.split(",")
        coordinates = [(float(c.split(":")[1]), float(c.split(":")[0])) for c in coordinates]

        stops = data['RouteStops']
        stop_info = [(float(stop['Lat']), float(stop['Lon']), stop['StopId']) for stop in stops]

        return coordinates, stop_info

    async def create_page(self, forward: str, language: str) -> str:
        html_name = f'{self.route_number}_forward_{forward}.html'
        existing_files = os.path.exists(f'home_page/routes/{self.route_number}_forward_{forward}.html')
        if not existing_files or config.REFRESH_HTML_FILES:
            # Fetch the route data and generate the map
            coordinates, stop_info = await self.__get_coord_info(forward)

            msg = MessageFormatter(language, 'webapp')
            # Make map with folium
            m = await FoliumWebAppBuilder(coordinates[0], msg, 14).webapp_bubble()

            folium.plugins.AntPath(coordinates, color="#3d00f7", delay=500, weight=2.5, opacity=1).add_to(m)

            for stop in stop_info:
                icon = folium.features.CustomIcon(os.path.join('data', 'static', 'media', 'bus_stop_icon.png'),
                                                  icon_size=[17, 17])  # Add custom icon

                text = f"{msg.get_message(format_dict={'bus_stop': 'none'})} " \
                       f"ID: <span id='mystop' " \
                       f"style='color: #ffffff; text-decoration: none; transition: color 0.3s ease;'>" \
                       f"{stop[2]}</span>"
                text = f"<div id='mytext' class='display_text' onclick='handleClick(this)'>{text}</div>"
                popup = folium.Popup(html=text, max_width=300)
                folium.Marker(location=(stop[0], stop[1]),
                              popup=popup,
                              icon=icon).add_to(m)
            m.fit_bounds(coordinates)  # Automatically adjust map to show the whole route
            m.save(os.path.join('home_page', 'routes', html_name))

        return html_name
