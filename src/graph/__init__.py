import requests
import socketio
import numpy as np
class Graph:
    def __init__(self, url) -> None:
        self.url = url #"/"

        self.active = False

        self.initalize_session()
        self.sio = sio = socketio.SimpleClient()
        self.sid = sio.sid
        self.joined = False
        if self.active:
            self.sio.connect(url)

            self.sio.emit('client')
        else:
            raise Exception("Connection to Graph Unavaliable at URL {}".format(url))


    
    def graph(self, data: np.ndarray,scale: int,size: int,position: dict,color: str) -> None:

        data=list(np.reshape(data, (data.size))) # Flatten

        self.sio.emit("point", {
            "event": "add",
            "points": data,
            "scale": scale,
            "size": size,
            "position":position,
            "color":color
        })





    def initalize_session(self):
        if requests.get(self.url + "status").status_code < 300:
            self.active = True
