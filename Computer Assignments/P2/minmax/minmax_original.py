from utils import *
import math
from utils import *

def get_chooser(depth):
    def temp(this_game_map: np.ndarray):
        return choose(this_game_map, depth)
    return temp
def min_value(this_game_map: np.ndarray, depth,turn):
    if depth == 0:
        return get_one_side_score(abs(turn) * (this_game_map == turn))
    v = np.inf
    for choice in list(zip(*np.where(get_available_points(this_game_map)))):
        copy_game = this_game_map.copy()
        copy_game[choice] = turn
        v = min(v, max_value(-copy_game, depth-1, -1 * turn))
    return v

def max_value(this_game_map: np.ndarray, depth,turn):
    if depth == 0:
        return get_one_side_score(abs(turn) * (this_game_map == turn))
    v = -np.inf
    for choice in list(zip(*np.where(get_available_points(this_game_map)))):
        copy_game = this_game_map.copy()
        copy_game[choice] = turn
        v = max(v,min_value(-copy_game,depth-1,-1*turn))
    return v
def choose(this_game_map: np.ndarray, depth):
    turn = 1
    best_choic = None
    v = -np.inf
    for choice in list(zip(*np.where(get_available_points(this_game_map)))):
        copy_game = this_game_map.copy()
        copy_game[choice] = turn
        value = min_value(-copy_game, depth - 1, -1 * turn)
        if v < value:
            best_choic = choice
            v = value
    return best_choic
