from sklearn.neighbors import KDTree
import numpy as np


def array_cord(bus_stops):
    # Создаем массив координат остановок и KD-дерево
    bus_stops_cords = np.array([[stop['lat'], stop['lon']] for stop in bus_stops])
    return KDTree(bus_stops_cords)
