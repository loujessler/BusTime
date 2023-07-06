import os
import folium.plugins as folium_plg

from bot.handlers.main.utils.folium_web_app_bld import FoliumWebAppBuilder
from bot.utils.additional import get_image_data
from bot.utils.data_utils.json_data import load_json_data
from bot.utils.localization.i18n import MessageFormatter


class PageBusStopsBuilder:
    def __init__(self, language):
        self.language = language

    async def create_page(self) -> str:
        html_name = f'bus_stops_info_{self.language}.html'
        existing_files = os.path.exists(f'home_page/bus_stops_info/bus_stops_info_{self.language}.html')
        icon = await get_image_data(os.path.join('data', 'static', 'media', 'bus_stop_icon.png'))
        if not existing_files:
            # Fetch the route data and generate the map
            stop_info = await load_json_data(f"stops_data")

            msg = MessageFormatter(self.language, 'webapp')
            # Make map with folium
            m = await FoliumWebAppBuilder([41.70329262810114, 44.79726756680793], msg).webapp_bubble()

            # Create a MarkerCluster object
            callback = ('function (row) {'
                        'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
                        'var icon = L.AwesomeMarkers.icon({'
                        "icon: 'info-sign',"
                        "iconColor: 'white',"
                        "markerColor: 'green',"
                        "prefix: 'glyphicon',"
                        "extraClasses: 'fa-rotate-0'"
                        '});'
                        'var icon = L.icon({'
                        'iconUrl: row[3],'
                        'iconSize: [16, 16],'
                        '});'
                        f'marker.setIcon(icon);'
                        "var popup = L.popup({maxWidth: '300'});"
                        "const display_text = {text: row[2]};"
                        "var mytext = $(`<div id='mytext' class='display_text' "
                        "style='width: 100.0%; height: 100.0%;'> ${display_text.text}</div>`)[0];"
                        f"popup.setContent(mytext);"
                        "marker.bindPopup(popup);"
                        'return marker};')
            data = [(stop['lat'],
                     stop['lon'],
                     f"{msg.get_message(format_dict={'bus_stop': 'none'})} "
                     f"ID: <a id='mystop' href='#' onclick='handleClick(this)'>{stop['code']}</a>",
                     icon) for stop in stop_info]
            folium_plg.FastMarkerCluster(data=data,
                                         callback=callback).add_to(m)
            # marker_cluster = folium_plg.MarkerCluster().add_to(m)
            #
            # for stop in stop_info:
            #     icon = folium.features.CustomIcon('./data/static/media/bus_stop_icon.png',
            #                                       icon_size=[18, 18])  # Add custom icon
            #     popup = f"{msg.get_message(format_dict={'bus_stop': 'none'})} " \
            #             f"ID: <a id='mystop' href='#' onclick='handleClick(this)'>{stop['code']}</a>"
            #     folium.Marker(location=(stop['lat'], stop['lon']),
            #                   popup=popup,
            #                   icon=icon).add_to(marker_cluster)  # Add markers to the MarkerCluster instead of map

            m.save(os.path.join('home_page', 'bus_stops_info', html_name))
        return html_name
