import math
import pygame as pyg
import networkx as nx
import random as rnd
from gameutil import *
from pygame import Vector2
from gameobj import GameObject
from itertools import combinations

# TODO: degree == 0 doesn't guarantee connections - fix this issue (e.g. consider case where
# map looks like: []--[]   []---[])
# TODO: improve the for n1, n2 in combinations approach because it seems like it could
# be quite inefficient for larger maps 
# TODO: modify the travel graph creation, so that the check for whether an object has at
# least one link is done within the edge generation loop instead of needing a separate one?
# TODO: improve the approach to checking if a rect is within line exclusion - potential for 
# program to get hung up if such an edge doesn't exist / can't be created?
# TODO: store the edges to be made before hand in the generate states? idk

OPINIONS = [
    "POSITIVE",
    "NEUTRAL",
    "NEGATIVE"
]
MIN_LEN = 100
LINE_EXCL_SF = 1.4 # TODO: Implement as part of the class

class GameMap:
    def __init__(self, seed: int, edge_chance: float, no_objs: int, obj_size: Vector2, res: tuple[int, int], excl_sf: float) -> None:
        # Attributes
        self.state_objs = []
        self.seed = seed
        self._excl_sf = excl_sf
        self._travel_graph = None
        self._opinion_graph = None
        
        rnd.seed(self.seed) # Set the seed for the random num gen

        self._generate_states(no_objs, obj_size, res, excl_sf, MIN_LEN)
        self._create_travel_graph(edge_chance)
        self._create_opinion_graph()
    
    def _reroll(self, no_objs: int, obj_size: int, res: tuple[int,int], excl_sf: float):
        self.state_objs = []
        self._travel_graph = nx.Graph()
        self._opinion_graph = nx.Graph()

    def _generate_states(self, no_objs: int, obj_size: Vector2, res: tuple[int,int], excl_sf: float, min_len: float):
        excl_list: list[GameObject] = []

        for i in range(no_objs):
            new_pos = rand_pos(res, obj_size)
            new_obj = GameObject(
                f"state{i}",
                Vector2(new_pos[0], new_pos[1]),
                Vector2(obj_size),
                color=(255,255,255)
            )

            valid = False
            while not valid:
                valid = True

                for o in excl_list:

                    # Test for rect exclusion overlap
                    excl = o.get_rect().scale_by(excl_sf)
                    new_obj_excl = new_obj.get_rect().scale_by(excl_sf)

                    if new_obj_excl.colliderect(excl):
                        new_pos = rand_pos(res, obj_size)
                        new_obj.set_pos(Vector2(new_pos))
                        
                        valid = False
                        break
                    
                    # Test for minimum distance 
                    dist = (new_obj.get_pos() - o.get_pos()).magnitude()
                    if dist < min_len:
                        new_pos = rand_pos(res, obj_size)
                        new_obj.set_pos(Vector2(new_pos))
                        
                        valid = False
                        break
            
            self.state_objs.append(new_obj)
            excl_list.append(new_obj)
    
    def _create_travel_graph(self, edge_chance: float) -> None:
        self._travel_graph = nx.watts_strogatz_graph(len(self.state_objs), 2, edge_chance, self.seed)

        replace_nodes(
            self.state_objs, 
            self._travel_graph, 
            lambda e : (e[0].get_pos() - e[1].get_pos()).magnitude(),
            "distance"
        )

        # Node splitting
        overlaps = 0
        for e in self._travel_graph.edges:
            others = self.state_objs.copy()
            others.remove(e[0])
            others.remove(e[1])

            for o in others:
                pdist = perp_dist(e[0].get_pos(), e[1].get_pos(), o.get_pos())
                if pdist != -1 and pdist < 30:
                    overlaps += 1
                    print(f"perp dist: {pdist}")
                    print(f"{o.alias} overlaps with {e[0].alias}---{e[1].alias}")

        print(f"overlaps: {overlaps}")
    
    # As of the current design, these won't be drawn as edges
    def _create_opinion_graph(self) -> None:
        self._opinion_graph = nx.complete_graph( len(self.state_objs) )

        replace_nodes(
            self.state_objs, 
            self._travel_graph, 
            lambda e : rnd.choice(OPINIONS),
            "opinion"
        )

        # Create mapping to change graph nodes into GameObjects
        mapping = {}
        for i in range( len(self.state_objs) ):
            mapping[i] = self.state_objs[i]
        
        nx.relabel_nodes(self._opinion_graph, mapping)
        for e in self._opinion_graph.edges:
            nx.set_edge_attributes(self._opinion_graph, rnd.choice(OPINIONS), "opinion")

    def draw(self, surf: pyg.Surface, db_drwexcl: bool = False, db_drwcent: bool = False, db_drwtopleft: bool = False):
        if db_drwexcl:
            for o in self.state_objs:
                pyg.draw.rect(surf, (128,0,0), o.get_rect().scale_by(self._excl_sf))
        
        # Draw travel links first
        for o1,o2 in self._travel_graph.edges:
            draw_dline(surf, (128,128,128), o1.get_pos(), o2.get_pos(), 4, 15)

        # Then draw states on top
        for o in self.state_objs:
            pyg.draw.rect(surf, o.color, o.get_rect())

            if db_drwtopleft:
                pyg.draw.circle(surf, (255,255,255), o.get_rect().topleft, 4)
                pyg.draw.circle(surf, (0,0,255), o.get_rect().topleft, 3)
            if db_drwcent:
                pyg.draw.circle(surf, (255,255,255), o.get_pos(), 4)
                pyg.draw.circle(surf, (255,0,0), o.get_pos(), 3)