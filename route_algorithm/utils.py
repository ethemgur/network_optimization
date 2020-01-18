import folium
from folium.features import DivIcon
from itertools import combinations
import numpy as np
from floyd import get_path
from time import time


def get_score(data, place1, place2, weights, prefs):
    score_params = get_score_params(data, place1, place2, prefs)
    score = sum([x * score_params[i] for i, x in enumerate(weights)])
    return score + 100


def timer(f):
    def inner(*args, **kwargs):
        start = time()
        rv = f(*args, **kwargs)
        end = time()
        print('\tElapsed time: {} seconds'.format(round(end - start, 2)))
        return rv
    return inner


def display_map(data):
    folium_map = folium.Map(location=[41, 28.95],
                            zoom_start=13,
                            tiles="CartoDB positron")

    points = []

    for i in data:
        lat = data[i]['lat']
        lon = data[i]['lon']
        points.append((lat, lon))
        folium.Marker(location=[lat, lon], icon=DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html='<div style="font-size: 10pt; color:black">{0}</div>'.format(data[i]['name']),)
        ).add_to(folium_map)
        folium_map.add_child(folium.CircleMarker([lat, lon], radius=6))

    # current_dir = os.path.dirname(os.path.realpath(__file__))
    # folium_map.save("{}/../templates/algorithm/my_map.html".format(current_dir))
    return folium_map._repr_html_()


def update_plot(path_obj):
    folium_map = folium.Map(location=[41, 28.95],
                            zoom_start=13,
                            tiles="CartoDB positron")

    points = []

    for i in path_obj:
        lat = i['lat']
        lon = i['lon']
        points.append((lat, lon))
        folium.Marker(location=[lat, lon], icon=DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html='<div style="font-size: 10pt; color:black">{0}</div>'.format(i['name']),)
        ).add_to(folium_map)
        folium_map.add_child(folium.CircleMarker([lat, lon], radius=6))

    folium.PolyLine(points, color="red", weight=2.5,
                    opacity=1).add_to(folium_map)
    # current_dir = os.path.dirname(os.path.realpath(__file__))
    # folium_map.save("{}/../templates/algorithm/my_map.html".format(current_dir))
    return folium_map._repr_html_()


def get_ahp_scores(ahp_sliders):
    ahp_scores = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        ahp_scores[i][i] = 1
    for i, x in enumerate(list(combinations(range(3), 2))):
        value = ahp_sliders[i][1].value
        if ahp_sliders[i][1].value < 0:
            ahp_scores[x[0]][x[1]] = (value * -1)
            ahp_scores[x[1]][x[0]] = 1 / (value * -1)
        else:
            ahp_scores[x[0]][x[1]] = 1 / value
            ahp_scores[x[1]][x[0]] = value
    return ahp_scores



def path_handler(data, sp, pred):
    sp_index = np.unravel_index(np.argmin(sp[:, :, -1]), sp.shape[:2])
    places = list(data.keys())
    path_ids = [places[i] for i in get_path(pred, sp_index[0], sp_index[1], sp.shape[2]-1)]
    path_names = [data[i]['name'] for i in path_ids]
    return path_ids, path_names


def get_score_params(data, place1, place2, prefs):
    distance = data[place1]['neighbours'][place2][0] / 10000
    rating, comment, category = 0, 0, 0
    for i in [place1, place2]:
        rating += data[i]['rating'] / 5 / 2
        comment += data[i]['rating_count'] / 45000 / 2
        category += len(set(data[i]['category']).intersection(prefs)) / 2

#     return [distance, distance, distance]

    return [distance, - (rating * comment), - category]

