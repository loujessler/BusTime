import os
import typing

import folium
import folium.plugins

from bot.handlers.main.ttc.ttc_requests.get_ttc_api import GetTTC
from bot.handlers.main.utils.folium_web_app_bld import FoliumWebAppBuilder
from bot.utils.additional import ConvertNumber
from bot.utils.data_utils.json_data import load_json_data
from bot.utils.localization.i18n import MessageFormatter


class PageRouteBuilder:
    def __init__(self, route_number: str):
        self.route_number = route_number
        self.route_data = {}

    async def _load_route_data(self, forward: typing.Union[str, int]):
        """
        Load data from json file and cache in class

        :param forward:
        :return:
        """
        if forward not in self.route_data:
            self.route_data[forward] = await load_json_data(f"routes/{self.route_number}_forward_{forward}")
        return self.route_data[forward]

    async def check_forwards(self) -> list:
        """
        Func check have forwarded in json
        :return:
        """
        have_forwards = []
        for forward in [0, 1]:
            data = await self._load_route_data(forward)
            shape = data['Shape']
            if shape != '':
                have_forwards.append(forward)
        return have_forwards

    async def get_route_directions(self, forwards: list, language: str) -> list:
        """
        Func get route direction and create list with text of directions

        :param forwards:
        :param language:
        :return:
        """
        route_directions = []
        for forward in forwards:
            data = await self._load_route_data(forward)

            # Извлечение данных о остановках
            stops = data['RouteStops']
            name = 'Name' if language == 'ka' else 'Name_translit'
            # Получение имени первой и последней остановки
            first_stop_name = stops[0][name]
            last_stop_name = stops[-1][name]
            route_directions.append(f"💢💢💢{ConvertNumber('forward_numbers').convert(forward)}💢💢💢\n"
                                    f" {first_stop_name} \n                ⬇️\n {last_stop_name}")
        return route_directions

    async def __get_coord_info(self, forward: str):
        """
        Func get coordinates from json

        :param forward:
        :return:
        """
        data = await self._load_route_data(forward)
        shape = data['Shape']
        coordinates = shape.split(",")
        coordinates = [(float(c.split(":")[1]), float(c.split(":")[0])) for c in coordinates]

        stops = data['RouteStops']
        stop_info = [(float(stop['Lat']), float(stop['Lon']), stop['StopId']) for stop in stops]

        return coordinates, stop_info

    async def _create_buses_markers(self, folium_map: FoliumWebAppBuilder, forward: str):
        """
        Func create bus's markers

        :param folium_map:
        :param forward:
        :return:
        """
        locations = await GetTTC().where_bus_info(self.route_number, forward)
        for location in locations:
            icon = folium.features.CustomIcon(os.path.join('data', 'static', 'media', 'bus_icon.png'),
                                              icon_size=[21, 21])  # Add custom icon
            folium.Marker(location=location, icon=icon).add_to(folium_map)

    async def create_page(self, forward: str, language: str) -> str:
        """
        Func create HTML page with bus's route

        :param forward:
        :param language:
        :return:
        """
        html_name = f'{self.route_number}_forward_{forward}.html'

        # Fetch the route data and generate the map
        coordinates, stop_info = await self.__get_coord_info(forward)
        msg = MessageFormatter(language, 'webapp')

        # Make map with folium
        m = await FoliumWebAppBuilder(coordinates[0], msg, 14).webapp_bubble()
        await self._create_buses_markers(m, forward)
        folium.plugins.AntPath(coordinates, color="#3d00f7", delay=2000, weight=2.5, opacity=1).add_to(m)

        icon_path = os.path.join('data', 'static', 'media', 'bus_stop_icon.png')
        local_bus_stop_name = msg.get_message(format_dict={'bus_stop': 'none'})
        for stop in stop_info:
            icon = folium.features.CustomIcon(
                icon_path,
                icon_size=[17, 30])  # Add custom icon

            text = f"<div id='mytext' class='display_text' onclick='handleClick(this)'>" \
                   f"{local_bus_stop_name} " \
                   f"ID: <span id='mystop' " \
                   f"style='color: #ffffff; text-decoration: none; transition: color 0.3s ease;'>" \
                   f"{stop[2]}</span></div>"
            popup = folium.Popup(html=text, max_width=300)
            folium.Marker(
                location=(stop[0], stop[1]),
                popup=popup,
                icon=icon).add_to(m)

        m.fit_bounds(coordinates)  # Automatically adjust map to show the whole route
        m.save(os.path.join('home_page', 'routes', html_name))

        return html_name
