import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import logging as log
import sys
import numpy as np


def compute_sparseness(map, x):
    n = len(map)
    # Sparseness is evaluated only if the archive is not empty
    # Otherwise the sparseness is 1
    if (n == 0) or (n == 1):
        sparseness = 0
    else:
        sparseness = density(map, x)
    return sparseness


def get_neighbors(b):
    neighbors = []
    neighbors.append((b[0], b[1]+1))
    neighbors.append((b[0]+1, b[1]+1))
    neighbors.append((b[0]-1, b[1]+1))
    neighbors.append((b[0]+1, b[1]))
    neighbors.append((b[0]+1, b[1]-1))
    neighbors.append((b[0]-1, b[1]))
    neighbors.append((b[0]-1, b[1]-1))
    neighbors.append((b[0], b[1]-1))

    return neighbors


def density(map, x):
    b = x.features
    density = 0
    neighbors = get_neighbors(b)
    for neighbor in neighbors:
        if neighbor not in map:
            density += 1
    return density


def get_distance(v1, v2):
    return np.linalg.norm(v1 - v2)


def check_overlaps(o1, o2):
    return False


def setup_logging(log_to, debug):

    def log_exception(extype, value, trace):
        log.exception('Uncaught exception:', exc_info=(extype, value, trace))

    # Disable annoyng messages from matplot lib.
    # See: https://stackoverflow.com/questions/56618739/matplotlib-throws-warning-message-because-of-findfont-python
    log.getLogger('matplotlib.font_manager').disabled = True

    term_handler = log.StreamHandler()
    log_handlers = [term_handler]
    start_msg = "Started test generation"

    if log_to is not None:
        file_handler = log.FileHandler(log_to, 'a', 'utf-8')
        log_handlers.append( file_handler )
        start_msg += " ".join(["writing to file: ", str(log_to)])

    log_level = log.DEBUG if debug else log.INFO

    log.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=log_level, handlers=log_handlers)

    sys.excepthook = log_exception

    log.info(start_msg)