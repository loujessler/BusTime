import folium
import folium.plugins

from bot.utils.localization.i18n import MessageFormatter


class FoliumWebAppBuilder(folium.Map):
    def __init__(self, location, msg_formatter: MessageFormatter, zoom: int):
        super().__init__(location=location, zoom_start=zoom)
        self.msg = msg_formatter
        self.get_root().html.add_child(folium.JavascriptLink('https://telegram.org/js/telegram-web-app.js'))
        self.get_root().html.add_child(folium.CssLink(
            'http://code.ionicframework.com/ionicons/1.5.2/css/ionicons.min.css'))

    async def webapp_bubble(self):

        # The map is already created by the parent class folium.Map
        # So, there is no need to create m = folium.Map(location=self.location, zoom_start=14)

        # You can now directly use the methods of folium.Map on self
        # For example, self.get_root() instead of m.get_root()

        js = f"""
        var WebApp = window.Telegram.WebApp;
        var MainButton = WebApp.MainButton;

        MainButton.show();

        MainButton.setText("{self.msg.get_message(format_dict={'close': 'none'})}")

        MainButton.onClick(function() {{
          WebApp.close();
        }});
        WebApp.onEvent('mainButtonClicked', function() {{
          /* also */
        }});
        """
        js = '<script type="text/javascript">' + js + '</script>'

        # Добавляем этот элемент на карту
        self.get_root().html.add_child(folium.Element(js))
        self.get_root().html.add_child(folium.JavascriptLink("../js/ttc/route_page.js"))

        return self  # Return the modified object itself
