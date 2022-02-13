import folium
import pandas


def get_elevation_colour(elevation):
    if (elevation < 1000):
        return 'green'
    elif (elevation > 1000 and elevation < 2000):
        return 'beige'
    elif (elevation > 2000 and elevation < 3000):
        return 'orange'
    elif (elevation > 3000):
        return 'red'


def get_population_colour(population):
    if (population < 10000000):
        return 'green'
    elif (population >= 10000000 and population < 30000000):
        return 'yellow'
    elif (population >= 30000000):
        return 'red'
    else:
        return 'blue'


volcano_data = pandas.read_csv('volcanoes.txt')
volcano_coordinates = volcano_data[[
    'NAME', 'ELEV', 'LAT', 'LON']].values.tolist()

map = folium.Map(
    location=[40.7608, -111.8910],
    zoom_start=6,
    tiles="Stamen Terrain"
)
icon_group = folium.FeatureGroup(name='Volcanoes')
marker_html = """
    <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
    Height: %sm
"""

for volcano in volcano_coordinates:
    name = volcano.pop(0)
    elevation = volcano.pop(0)
    color = get_elevation_colour(int(elevation))
    iframe = folium.IFrame(
        html=marker_html % (name, name, str(elevation)),
        width=200,
        height=50
    )
    icon_group.add_child(
        folium.Circle(
            location=volcano,
            fill_color=color,
            color='black',
            fill_opacity=0.7,
            radius=5000,
            popup=folium.Popup(iframe),
        ),
    )

population_group = folium.FeatureGroup(name='Population')
population_data_polygon = open('world.json', 'r', encoding='utf-8-sig').read()
population_group.add_child(
    folium.GeoJson(
        population_data_polygon,
        style_function=lambda country: {
            'fillColor': get_population_colour(country['properties']['POP2005'])
        }
    )
)

map.add_child(icon_group)
map.add_child(population_group)
map.add_child(folium.LayerControl())
map.save("volcanoes.html")
