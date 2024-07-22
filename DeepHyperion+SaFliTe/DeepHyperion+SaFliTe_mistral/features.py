
import math

def compute_distance(ind):
    """
    computes euclidean distance between center of two obstacles
    """
    x1 = ind.obstacle1.position.x
    y1 = ind.obstacle1.position.y
    x2 = ind.obstacle2.position.x
    y2 = ind.obstacle2.position.y  

    distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
    return round(distance, 1)

def compute_height(ind):
    """
    computes height difference between center of two obstacles
    """
    h1 = ind.obstacle1.size.h
    h2 = ind.obstacle2.size.h
    delta_h = abs(h2 - h1)
    return round(delta_h, 1)

def compute_angle(ind):
    """
    computes angle difference between the center of two obstacles
    """
    x1 = ind.obstacle1.position.x
    y1 = ind.obstacle1.position.y
    x2 = ind.obstacle2.position.x
    y2 = ind.obstacle2.position.y 
    delta_degree = math.degrees(math.atan2(y2-y1, x2-x1))

    return round(delta_degree, 1)