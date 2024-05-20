from flask import Flask, Response, join_room, leave_room, render_template, url_for, request
from flask_socketio import SocketIO, send,emit
from uuid import uuid4
from typing import Type
from math import floor
from shapes import *

class Data:

    def __init__(self, sync_db = False) -> None:
        self.app = Flask(__name__, 
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
        self.app.config['SECRET_KEY'] = 'secret!'
        self.socketio = SocketIO(self.app)
        # Objects
        """
        BOX EXAMPLE
        {
                "uuid": "BONJOUR",
                "type": "box",
                "scale": {
                    "x":1, "y": 1, "z": 1
                },"position": {
                    "x":x, "y": 1, "z": 1
                } "color": 8008
                
            } for x in range(0, 10, 2)

        POINT CLOUD EXAMPLE
        {
                "uuid":"sdfsdf",
                "type":"point cloud",
                "scale":10,
                "size":1,
                "position": {
                    "x":1, "y": 1, "z": 1
                },"points" : [
                0, 0, 0,
                0, 0, 1,
                0, 0, 2,
                ], "color": 88808
        } 
        """
        self._objects = [
            
        ]
        
        # Clients
        self.clients = {

        }

        # Data Providers
        self.providers = {

        }

        # Methods Define
        @self.app.route("/")
        def home():
            return {"client":url_for("client")}

        @self.app.route("/status")
        def status():
            return Response("Good!", 200)


        @self.app.route('/client')
        def client():
            

            return render_template("index.html")
        
        @self.app.route("/box/")
        def new_box():
            self.objects = Box({"x":1,"y":1,"z":1}, {"x":1,"y":1,"z":1},9009)
            return str(self.objects)
        @self.app.route("/pc/")
        def new_pc():
            self.objects = Point_Cloud(1, 1, {"x":1,"y":1,"z":1}, 1111, [floor(x/3) for x in range(36)])
            return str(self.objects)
        
        @self.socketio.on('connect')
        def connection():
            print("Client Connected with SID of {}".format(request.sid))
        @self.socketio.on('init')
        def start(data):
            _id = str(request.sid)
            self.clients[_id] = {
                "id": _id, "sync": False
            }
            print("Client ({}) requests to initalize and sync".format(_id))
            emit("text", {"text": "Syncing", "time":1000})
            emit("sync", {
                "len": 10,
                "sid": _id,
                "objects": self.objects
            }, to=_id)
            print("Client ({}) finished sync".format(_id))
        
        # TODO Add on Box, and Point Cloud to server to cache so new instances will open with them

           
 
    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, n_box: Type[Shape]):
        #for c, _object in enumerate(self.objects): 
        #    if (_object["uuid"] == n_box["uuid"]):
                # TODO Edit Keys Here
        #        self.objects[c] == n_box
        #        return
        # No Refrences Exsist, Adding New   
        # Add Refrence for SYNC to work           
        self.objects.append(n_box.as_dict())
        
        if type(n_box) is Box:
            # Universal Broadcast to exsisting ones
            self.socketio.emit("box", n_box.as_dict())
        elif type(n_box) is Point_Cloud:
            self.socketio.emit("point", n_box.as_dict())

    def run(self):
        d.socketio.run(d.app,debug=True)


d = Data()




    
if __name__ == '__main__':
    #d.objects = Box({"x":1,"y":1,"z":1}, {"x":1,"y":1,"z":1},9009)
    #d.objects = Box({"x":1,"y":1,"z":1}, {"x":2,"y":1,"z":1},9009)
    d.run()
