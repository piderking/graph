import requests
import numpy as np
from shapes import *
class Graph:
    def __init__(self, url) -> None:
        self.url = url if url[-1] == "/" else url + "/" #"/"


      
        
        if self.initalize_session():
            print("API Ready")
        #self.graph(np.array([x for x in range(36)]), 1, 1, {"x":1,"y":1,"z":1}, 9111)
        print("Done")

    def box(self, scale, position, color, event):
         requests.get(self.url + "", json=Box(scale, position, color, event=event))
    def graph(self, data: np.ndarray,scale: int,size: int,position: dict,color: str) -> str:

        data=list(np.reshape(data, (data.size))) # Flatten
        data = [float(d) for d in data]

        req = requests.get(self.url + "point", json=Point_Cloud(
            scale, size, position, color, data, event="add"
        ).as_dict())

        return req.json()[0]["uuid"]
    
    def removeObject(self, uuid: str, type: str) -> dict:
        req = requests.get(self.url + "remove", json={"uuid":uuid, "type":type})
        return req.json
    





    def initalize_session(self):
        if requests.get(self.url + "status").status_code < 300:
            return True
        return False
