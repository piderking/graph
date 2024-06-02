import requests
import numpy as np
from .shapes import Point_Cloud, Box, Shape
from .util.config import URL


class Graph:
    """Instance of a hosted graph (move objects and interact with them)
    """
    def __init__(self, url: str or None=URL, uid="admin", passkey="admin") -> None:
        """Create an instance to a hosted graph (see server package)

        Args:
            url (strorNone, optional): _description_. Defaults to URL.
        """
        if url is None:
            self.url = URL
        self.url = url if url[-1] == "/" else url + "/" #"/"
        self.passkey = passkey
        self.uid = uid
        self.code = None
        if self.initalize_session():
            print("API Ready")

    @PendingDeprecationWarning
    def box(self, scale: dict["x/y/z":float], position: dict["x/y/z":float], color:int, event: str):
        """Box objects will be depreacted soon
        """
        requests.get(self.url + "", json=Box(scale, position, color, event=event))

    @staticmethod
    def reshape(data: np.ndarray) -> np.ndarray:
        """Reshape into the correct figure of array (1 dimensional)

        Args:
            data (np.ndarray): [[x1,y1,z1],[x2,y2,z2]] => [x1,y1,z1,x2,y2,z2]

        Returns:
            np.ndarray: 1D Array
        """
        data=list(np.reshape(data, (data.size))) # Flatten
        data = [float(d) for d in data]
        return data

    def graph(self, point_cloud: Point_Cloud) -> str:
        """Graph a Point Cloud Object

        Args:
            point_cloud (Point_Cloud): The point cloud object which is being accessed

        Returns:
            str: uuid of object (should be the same)
        """

        req = requests.get(self.url + "point", json=point_cloud.as_dict())

        return dict(req.json())["uuid"]

    def removeObject(self, uuid: str, type: str) -> dict:
        req = requests.get(self.url + "remove", json={"uuid":uuid, "type":type})
        return req.json

    def moveObject(self, uuid: str, type: str, x:float, y:float, z:float) -> dict:
        req = requests.get(self.url + "move", json={"uuid":uuid, "type":type, "position":{"x":x, "y":y, "z":z}})
        return req.json

    def scaleObject(self, uuid: str, type: str, x:float, y:float, z:float) -> dict:
        req = requests.get(self.url + "move", json={"uuid":uuid, "type":type, "scale":{"x":x, "y":y, "z":z}})
        return req.json
    def setPointSize(self, uuid: str, type: str, x:float, y:float, z:float) -> dict:
        req = requests.get(self.url + "move", json={"uuid":uuid, "type":type, "scale":{"x":x, "y":y, "z":z}})
        return req.json






    def initalize_session(self):
        req = requests.get(self.url + "status", json={
            "id":self.uid,
            "passkey":self.passkey,
            "create":True,
        }, headers={'Authorization': 'uid:peter'})
        if req.status_code < 300:
            self.code = req.json()["code"]
            return req.json
        raise Exception("Session UnAuthorized! " + str(req.json()))
