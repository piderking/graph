import requests
import numpy as np
from .shapes import Point_Cloud, Box, Shape
from .util.config import URL
import json

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

        req = requests.get(self.url + "point", json=point_cloud.as_dict(),headers={'Authorization': json.dumps({"id":self.uid, "code":self.code})})
        if req.status_code < 300:
            return dict(req.json())["uuid"]
        else:
            print(req.content)
            return

    def removeObject(self, uuid: str) -> dict:
        obj: Point_Cloud = Point_Cloud.from_uuid(self.url, uuid)
        obj.remove()
        return obj

    def moveObject(self, uuid: str, x:float, y:float, z:float) -> dict:
        obj: Point_Cloud = Point_Cloud.from_uuid(self.url, uuid)
        obj.move(x, y, z)
        return obj
    def scaleObject(self, uuid: str, x:float, y:float, z:float) -> dict:
        obj: Point_Cloud = Point_Cloud.from_uuid(self.url, uuid)
        obj.scale(x, y, z)
        return obj
    def setPointSize(self, uuid: str,size:float) -> dict:
        obj: Point_Cloud = Point_Cloud.from_uuid(self.url, uuid)
        obj.set_size(size)
        return obj

    def setPointSize(self, uuid: str,color:int) -> dict:
        obj: Point_Cloud = Point_Cloud.from_uuid(self.url, uuid)
        obj.set_color(color)
        return obj


 






    def initalize_session(self):
        req = requests.get(self.url + "status", json={
            "id":self.uid,
            "passkey":self.passkey,
            "create":True,
        })
        if req.status_code < 300:
            self.code = req.json()["code"]
            return req.json
        raise Exception("Session UnAuthorized! " + str(req.json()))
