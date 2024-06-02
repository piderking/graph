from typing import Self
from uuid import uuid4
from abc import abstractmethod
import requests
from .util.config import URL
from .exceptions import ShapeNotFound, NoURLSpecified
import numpy as np
class Shape:
    uuid = str(uuid4())
    _type: str = "shape"
    url: str = URL
    def __init__(self, url, uuid: str or None):
        """Create a new Shape Class

        Args:
            url (str): URL of Graph (Provided)
            uuid (str): UUID of object, if none it will be generated (optional)
        """
        if not url is None: self.url = url
        if not uuid is None: self.uuid = uuid
    
    def validURL(self):
        if self.url is None: raise NoURLSpecified(self._type)
    
    def move(self, sx, sy, sz) -> bool:
        """Move the Object on the graph

        Args:
            sx (_type_): _description_
            sy (_type_): _description_
            sz (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.validURL()
        res = requests.get(self.url + "point", json={
            "uuid": self.uuid,
            "event": "move",
            "position": {
                "x":sx,
                "y":sy,
                "z":sz,
            }
        })
        if res.status_code < 300:
            return True
        else:
            return res.json()["reason"]
    def scale(self, sx, sy, sz):
        self.validURL()

        res = requests.get(self.url + "point", json={
            "uuid": self.uuid,
            "event": "scale",
            "position": {
                "x":sx,
                "y":sy,
                "z":sz,
            }
        })
        if res.status_code < 300:
            return True
        else:
            return res.json()["reason"]
        
    def set_color(self, color:int):
        self.validURL()

        res = requests.get(self.url + "point", json={
            "uuid": self.uuid,
            "event": "set_color",
            "color": color
        })
        
        if res.status_code < 300:
            return True
        else:
            return res.json()["reason"]
        
    def set_size(self, size:int):
        self.validURL()

        res = requests.get(self.url + "point", json={
            "uuid": self.uuid,
            "event": "set_size",
            "size": size
        })
        
        if res.status_code < 300:
            return True
        else:
            return res.json()["reason"]
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

        super().__init__(url, uuid=uuid)



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
    """Create a point cloud

    """
    @staticmethod
    def reshape(data: np.ndarray or list) -> np.ndarray:
        data=np.array(data)
        data=list(np.reshape(data, (data.size))) # Flatten
        data = [float(d) for d in data]
        return data
    
    def __init__(self, url: str or np.ndarray or None, points: list, scale: dict={"x":1,"y":1, "z":1}, size: int = .1, position: dict = {"x":0,"y":0, "z":0}, color: int = 9001, event: str = "add", uuid: None or str = None, lines: bool = False, connections:list=[], font_url: str = "fonts/lmk.json") -> None:
        """Point Cloud Object Representation

        Args:
            url (str): URL of Graph 
            points (list or np.ndarray): 
            scale (dict): Scale qualifier for each axis. Defaults to {"x":1,"y":1, "z":1}.
            size (int,): Point Size on Point cloud. Defaults to .1
            position (dict): 3D Vector Position. Defaults to {"x":0,"y":0, "z":0}.
            color (int): Color value. Defaults to 9001. (Blue)
            event (str): Event type "add", "remove", "move", "scale", "set_size", "set_color". Defaults to "add".
            uuid (None or str): The UUID (optional) Defaults to None.
            lines (bool): Include connection Defaults to False.
            connections (list): List of [landmark#1,landmark#2,line_size,color] Defaults to [].
            font_url (str):  URL to font of text. Defaults to "fonts/lmk.json".
        """
        self._type = "point cloud"
        self.scale = scale
        self.position = position
        self.color = color
        self.size = size
        self.point = Point_Cloud.reshape(points)
        self.event = event
        self.uuid = uuid if not uuid is None else self.uuid
        self.lines = lines
        self.conections = connections
        self.font_url = "fonts/lmk.json" if font_url is None else font_url

        super().__init__(url, uuid)

    def as_dict(self):
        """Generate a dictionary from the passed arguements

        Returns:
            (dict): Dictionary of specified data
                - connection kwarg is "additional_connections" in dictionary
                - not all must be specified -- can be used to construct events
        """
        return {
                "url": self.url,
                "uuid": self.uuid,
                "type": self._type,
                "scale": self.scale,
                "size": self.size,
                "position": self.position,
                "color": self.color,
                "points": self.point,
                "event": self.event,
                "lines": self.lines,
                "font_url": self.font_url,
                "additional_connections": self.conections
            }
    @staticmethod
    def from_dict(data: dict) -> Self:
        """Construct a Point Cloud instance from a dictionary

        Args:
            data (dict): Dictionary
                - connection kwarg is "additional_connections" in dictionary
                - not all must be specified -- can be used to construct events

        Returns:
            Point_Cloud: Point Cloud Object representation of the data
        """
        return Point_Cloud(
            data["url"],
            data["points"],
            scale=data["scale"],
            size=data["size"],
            position=data["position"],
            color=data["color"],
            event=data["event"],
            lines=data["lines"],
            font_url=data["font_url"],
            connections=data["additional_connections"],

        )
    @staticmethod
    def from_uuid(url: str, _uuid: str):
        """Generate a Point Cloud object from a UUID on a graph

        Args:
            url (str): URL of Server
            _uuid (str): UUID of saved object

        Returns:
            Point_Cloud: The Point Cloud from the UUID
        """
        res = requests.get(url + "point/" + _uuid)
        if res.status_code < 200:
            return Point_Cloud.from_dict(dict(res.json()))
        else:
            raise ShapeNotFound(type="Point Cloud")
