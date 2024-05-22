from uuid import uuid4
from abc import abstractmethod
class Shape:    
    uuid = str(uuid4())
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
    def __init__(self, scale: dict, position: dict, color: str or int, event: str = "add", uuid: None or str = None) -> None:
        self.scale = scale
        self.position = position
        self.color = color
        self.event = event
        self.uuid = uuid if not uuid is None else self.uuid
    def move(self, x, y, z):
        pass # TODO Implement Move Feature

    def scale(self, sx, sy, sz):
        pass
    def as_dict(self):
        return {
                "uuid": self.uuid,
                "type": "box",
                "scale": self.scale,
                "position": self.position,
                "color": self.color,
                "event": self.event       
            }
    @staticmethod
    def from_dict(data):
        return Box(data["scale"], data["position"], data["color"], event=data["event"], uuid=data["uuid"])
    
class Point_Cloud(Shape):
    def __init__(self, scale: int, size: int, position: dict, color: str or int, points: list, event: str = "add", uuid: None or str = None, lines=False, text=False) -> None:
        self.scale = scale
        self.position = position
        self.color = color
        self.size = size
        self.point = points
        self.event = event
        self.uuid = uuid if not uuid is None else self.uuid
        self.lines = lines
        self.text = text
    def move(self, x, y, z):
        pass # TODO Implement Move Feature

    def scale(self, sx, sy, sz):
        pass
    def as_dict(self):
        return {
                "uuid": self.uuid,
                "type": "point cloud",
                "scale": self.scale,
                "size": self.size,
                "position": self.position,
                "color": self.color,
                "points": self.point,
                "event": self.event,
                "lines": self.lines,
                "text": self.text     
            }
    @staticmethod
    def from_dict(data: dict):
        return Point_Cloud(data["scale"], data["size"], data["position"], data["color"], data["points"], event=data["event"], uuid=data["uuid"], lines=data["lines"], text=data["text"])