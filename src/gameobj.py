from pygame import Vector2, Color, Rect
from typing import Optional

class GameObject:
    def __init__(
            self, 
            alias: str, 
            pos: Vector2, 
            size: Vector2, 
            velocity: Optional[Vector2] = None, 
            color: Color = Color(255,255,255)
        ) -> None:
        
        self._rect = Rect(0,0,0,0)

        self.alias = alias
        self._pos = pos
        self._rect.x = pos.x - (size.x // 2)
        self._rect.y = pos.y - (size.y // 2)

        self.size = size
        self._rect.w = size.x
        self._rect.h = size.y

        if velocity == None:
            self.velocity = Vector2(0,0)
        else:
            self.velocity = velocity

        if color == None:
            self.color = Color(0,0,0)
        else:
            self.color = color
    
    def get_pos(self) -> Vector2:
        return self._pos

    def set_pos(self, pos: Vector2) -> None:
        self._pos = pos

        # Adjust rect pos based on object pos
        self._rect.x = pos.x - (self.size.x // 2)
        self._rect.y = pos.y - (self.size.y // 2)
    
    def set_size(self, size: Vector2) -> None:
        self.size = size

        self._rect.width = size.x
        self._rect.height = size.y

    def get_rect(self) -> Rect:
        return self._rect
    
    def __str__(self):
        return f"Alias: {self.alias} \nPos: <{self._pos.x}, {self._pos.y}> \nSize: {self.size.x}x{self.size.y} \nVelocity: <{self.velocity.x}, {self.velocity.y}> \nColor: {self.color} \nRect: {self._rect}\n"