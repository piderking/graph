from uuid import uuid4
from abc import abstractmethod
class Shape:    
    
    @abstractmethod
    def __init__(self) -> None:
        pass 
    @abstractmethod
    def move(self, x, y, z):
        pass # TODO Implement Move Feature
    @abstractmethod
    def scale(self, sx, sy, sz):
        pass
    @abstractmethod
    def as_dict(self):
        return {}
    def __repr__(self) -> str:
        return str(self.as_dict()) 
    

class Box(Shape):
    def __init__(self, scale: dict, position: dict, color: str or int, event: str = "add") -> None:
        self.scale = scale
        self.position = position
        self.color = color
        self.event = event
    def move(self, x, y, z):
        pass # TODO Implement Move Feature

    def scale(self, sx, sy, sz):
        pass
    def as_dict(self):
        return {
                "uuid": str(uuid4()),
                "type": "box",
                "scale": self.scale,
                "position": self.position,
                "color": self.color,
                "event": self.event       
            }
class Point_Cloud(Shape):
    def __init__(self, scale: int, size: int, position: dict, color: str or int, points: list, event: str = "add") -> None:
        self.scale = scale
        self.position = position
        self.color = color
        self.size = size
        self.point = points
        self.event = event

    def move(self, x, y, z):
        pass # TODO Implement Move Feature

    def scale(self, sx, sy, sz):
        pass
    def as_dict(self):
        return {
                "uuid": str(uuid4()),
                "type": "point cloud",
                "scale": self.scale,
                "size": self.size,
                "position": self.position,
                "color": self.color,
                "points": self.point,
                "event": self.event       
            }