
import folium
from folium.plugins import MeasureControl

from html2image import Html2Image
from geopy.geocoders import Nominatim

from hktg import db

KH_CENTER=[49.9989, 36.2473]

if __name__ == '__main__':
    geolocator = Nominatim(user_agent="pekelna-kitchen-bot")
    # location = geolocator.geocode("Харків Амосова 1")
    # print(location.address)

    m = folium.Map(
        location=KH_CENTER,
        zoom_start=12,
        control_scale=True,
        png_enabled=True
    )

    civils = db.get_table(db.Civil)
    locations = []
    for civil in civils:
        coords = civil.coords()
        if coords:
            locations.append((float(coords.latitude), float(coords.longitude)))
        else:
            location = geolocator.geocode(civil.address)
            locations.append((location.latitude, location.longitude))
        m.add_child(folium.Marker(
            locations[-1],
            popup=civil.address,
        ))

    m.add_child(folium.LatLngPopup())
    m.add_child(MeasureControl())
    m.add_child(folium.vector_layers.PolyLine(
                    locations,
                    # color=random_color,
                    tooltip="hello"
                ))


    # html = m._repr_html_() 
    html = m.save('index.html')
    # imgkit.from_file('index.html', 'out.jpg')
    hti = Html2Image()
    hti.screenshot(html_str='index.html', save_as='page.png')
    # out = m._to_png(5)
    # print(out)
