import os
import folium
import folium.plugins as folium_plg

from bot.handlers.main.utils.folium_web_app_bld import FoliumWebAppBuilder
from bot.utils.additional import number_to_emoji
from bot.utils.data_utils.json_data import load_json_data
from bot.utils.localization.i18n import MessageFormatter
from data import config


class PageBusStopsBuilder:
    def __init__(self, language):
        self.language = language

    async def create_page(self) -> str:
        existing_files = os.path.exists(f'home_page/bus_stops_info/bus_stops_info_{self.language}.html')
        if existing_files:
            # If file already exists, just send the first match
            html_name = f'bus_stops_info.html'
        else:
            # Fetch the route data and generate the map
            stop_info = await load_json_data(f"stops_data")

            msg = MessageFormatter(self.language, 'webapp')
            # Make map with folium
            m = FoliumWebAppBuilder([41.70329262810114, 44.79726756680793], msg)

            # Create a MarkerCluster object
            marker_cluster = folium_plg.MarkerCluster().add_to(m)

            for stop in stop_info:
                icon = folium.features.CustomIcon('./data/static/media/bus_stop_icon.png',
                                                  icon_size=[18, 18])  # Add custom icon
                popup = f"{msg.get_message(format_dict={'bus_stop': 'none'})} " \
                        f"ID: <a id='mystop' href='#' onclick='handleClick(this)'>{stop['code']}</a>"
                folium.Marker(location=(stop['lat'], stop['lon']),
                              popup=popup,
                              icon=icon).add_to(marker_cluster)  # Add markers to the MarkerCluster instead of map
            html_name = f'bus_stops_info_{self.language}.html'
            m.save(os.path.join('home_page', 'bus_stops_info', html_name))

        return html_name
