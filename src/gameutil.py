import math
import random as rnd
import pygame as pyg
import networkx as nx
from typing import Optional
from gameobj import GameObject
from collections.abc import Callable
from pygame import Surface, Vector2, Color

def interval_split(supintrv: list[int], subintrv: list[int]) -> list[list[int]]:
    return [[supintrv[0], subintrv[0] - 1], [subintrv[1] + 1, supintrv[1]]]

def deep_interval_split(intervals: list[list[int]], subintrv: list[int]) -> list[list[int]]:
    """
    INCLUDE BETTER EXPLANATION
    """

    # Find best-fit interval - if none exists, don't split anything
    bf_index = find_best_fit_interval(intervals, subintrv)
    if bf_index == -1:
        return intervals
    
    new_intrvs = interval_split(intervals[bf_index], subintrv)
    result = intervals.copy()

    # Remove old interval that will be split
    result.pop(bf_index)
    result.append(new_intrvs[0]); result.append(new_intrvs[1])
    result.sort()

    return result

def rand_interval(intervals: list[list[int]]) -> int:
    upper = len(intervals) - 1
    intrv = intervals[ rnd.randint(0, upper) ]

    if len(intrv) != 2:
        raise Exception("Interval lists must have a length of 2.")

    return rnd.randint(intrv[0], intrv[1])

def find_best_fit_interval(intervals: list[list[int]], test_intrv: list[int]) -> list[int]:
    for i in range(len(intervals)):
        if test_intrv[0] > intervals[i][0] and test_intrv[1] < intervals[i][1]:
            return i
    
    # If no best-fit interval found, return -1
    return -1

def draw_dline(surf: Surface, col: Color, start: tuple[int, int], end: tuple[int, int], width: int, dlen: int):
    startv = Vector2(start[0], start[1])
    endv = Vector2(end[0], end[1])

    # Direction vector to be used in drawing and incrementing the effective start point
    dirv = (endv - startv).normalize()
    eff_start = startv

    line_len = (endv - startv).magnitude()
    curr_len = 0
    while curr_len < line_len:
        pyg.draw.line(surf, col, eff_start, eff_start + (dlen*dirv), width)

        eff_start += 2 * dlen * dirv
        curr_len += 2 * dlen

def rand_pos(res: tuple, obj_size: Vector2):
        return Vector2(
            rnd.randint(obj_size.x // 2, (res[0]-1) - (obj_size.x // 2)), 
            rnd.randint(obj_size.y // 2, (res[1]-1) - (obj_size.y // 2))
        )

def perp_dist(a: Vector2, b: Vector2, p: Vector2) -> float:
    ab = b - a
    ap = p - a
    proj_c = ab.dot(ap) / (ab.magnitude()**2)

    # Check that the point is even "within" the line AB
    if 0 <= proj_c and proj_c <= 1:
        proj = a + (proj_c * ab)
        return (p - proj).magnitude()
    else:
        return -1

def replace_nodes(node_list: list, graph: nx.Graph, attr_func: Optional[Callable] = None, attr_name: Optional[str] = None) -> None:
        mapping = {}
        for i in range( len(node_list) ):
            mapping[i] = node_list[i]
        nx.relabel_nodes(graph, mapping, False)

        # Give each edge a single attribute, potentially based on the edge nodes themselves - if attribute function arg is given
        if attr_func:
            attr_map = {}
            for e in graph.edges:
                attr_map[e] = attr_func(e)
            nx.set_edge_attributes(graph, attr_map, attr_name)#

def split_link_by_game_obj(graph: nx.Graph, edge: tuple[GameObject, GameObject], node: GameObject) -> None:
    e1 = (edge[0], node)
    e2 = (node, edge[1])

    graph.remove_edge(edge)
    graph.add_edges_from([e1,e2])
