from uuid import uuid4
from abc import abstractmethod
import requests
from .util.config import URL
class Shape:    
    uuid = str(uuid4())
    _type: str = "shape"
    url: str = URL
    def __init__(self, url):
        if not url is None: self.url = url
    def move(self, sx, sy, sz) -> bool:
        """Move the Object on the graph

        Args:
            sx (_type_): _description_
            sy (_type_): _description_
            sz (_type_): _description_

        Returns:
            _type_: _description_
        """
        res = requests.get(self.url + "point", json={
            "uuid": self.uuid,
            "type": self._type,
            "position": {
                "x":sx,
                "y":sy,
                "z":sz,
            }
        })
        if res.status_code < 300:
            return True
        else:
            return res.json["exsists"]
    def scale(self, sx, sy, sz):
        res = requests.get(self.url + "point", json={
            "uuid": self.uuid,
            "type": self._type,
            "position": {
                "x":sx,
                "y":sy,
                "z":sz,
            }
        })
        if res.status_code < 300:
            return True
        else:
            return res.json
    @abstractmethod
    def as_dict(self):
        return {
            "uuid": self.uuid
        }
    def __repr__(self) -> str:
        return str(self.as_dict()) 
    


class Box(Shape):
    def __init__(self, scale: dict, position: dict, color: str or int, event: str = "add", uuid: None or str = None, url:str or None = None) -> None:
        self._type = "box"
        self.scale = scale
        self.position = position
        self.color = color
        self.event = event
        self.uuid = uuid if not uuid is None else self.uuid

        super().__init__(url)

       

    def as_dict(self):
        return {
                "uuid": self.uuid,
                "type": self._type,
                "scale": self.scale,
                "position": self.position,
                "color": self.color,
                "event": self.event       
            }
    @staticmethod
    def from_dict(data):
        return Box(data["scale"], data["position"], data["color"], event=data["event"], uuid=data["uuid"])
    
class Point_Cloud(Shape):
    def __init__(self, scale: int, size: int, position: dict, color: str or int, points: list, event: str = "add", uuid: None or str = None, lines=False, text=False, url: str or None = None) -> None:
        self._type = "point cloud"
        self.scale = scale
        self.position = position
        self.color = color
        self.size = size
        self.point = points
        self.event = event
        self.uuid = uuid if not uuid is None else self.uuid
        self.lines = lines
        self.text = text

        super().__init__(url)

    def move(self, x, y, z):
        
        pass # TODO Implement Move Feature

    def scale(self, sx, sy, sz):
        pass
    def as_dict(self):
        return {
                "uuid": self.uuid,
                "type": self._type,
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