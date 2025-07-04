import math
import random as rnd
import pygame as pyg
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

def perp_dist(p1: Vector2, p2: Vector2, p0: Vector2):
    numer = abs( ((p2.y - p1.y)*p0.x) - ((p2.x - p1.x)*p0.y) + (p2.x*p1.y) - (p2.y*p1.y) )
    denom = math.hypot(p1.x - p2.x, p1.y - p2.y)

    return numer / denom