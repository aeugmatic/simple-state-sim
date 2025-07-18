from typing import Optional
from gameobj import GameObject
from pygame import Vector2, Color

class PopulationObject(GameObject):
    def __init__(
            self, 
            alias: str, 
            pos: Vector2, 
            size: Vector2, 
            velocity: Optional[Vector2] = None, 
            color: Color = Color(255,255,255),
            population: int = 0,
            food: int = 0,
            water: int = 0,
            stability: int = 0
        ) -> None:
        
        super().__init__(alias, pos, size, velocity, color)
        self.population = population
        self.food = food
        self.water = water
        self.stability = stability