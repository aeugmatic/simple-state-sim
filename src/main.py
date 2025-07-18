# - FIXME: Properly figure out reseting the game map, current approach is buggy (test yourself to see the issue, cba writing it here right now)
# - !!!FIXME!!!: clean up the code so it's much neater and cleaner than it may be currently

import sys
import pygame as pyg
import random
from pygame import Vector2
from gamemap import GameMap
from pygame.locals import *

# Constants and other
MIN_RES = Vector2(640,480)
FPS = 60
S_LIM = 4
S_SIZE = 65
EXCL_SF = 2.0

SEED = random.randint(0, 2**32 - 1)

# Functions
def init_window(res, title):
    pyg.init()
    pyg.display.set_caption(title)
    
    screen = pyg.display.set_mode(res)
    clk = pyg.time.Clock()

    return screen, clk

def exit_window():
    pyg.quit()
    sys.exit()

def handle_events(events: list[pyg.event.Event], game_map: GameMap):
    for e in events:
        if e.type == QUIT:
            exit_window()
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                game_map._generate_states(S_LIM, Vector2(S_SIZE), MIN_RES, EXCL_SF)

def main(minres: tuple[int,int], fps: tuple[int,int]):
    min_screen, clk = init_window(minres, "Graph Draw Test")

    gmap = GameMap(SEED, 0.6, S_LIM, Vector2(S_SIZE), minres, EXCL_SF, db_printsplits=True)

    while True:
        handle_events(pyg.event.get(), gmap)

        min_screen.fill((0,0,0))
        gmap.draw(min_screen, db_drwexcl=False, db_drwcent=False, db_drwtopleft=False, db_aliastxt=True)

        pyg.display.update()
        clk.tick(fps)   

# Main
main(MIN_RES, FPS)
exit_window()