from flask import Flask, Response, render_template, url_for, request
from flask_socketio import SocketIO, send,emit
from uuid import uuid4
from typing import Type
from math import floor
from shapes import *

def dict_to_table(dic: dict) -> None:
    """Visual Representation

    Args:
        dic (dict): _description_
    """
    _str = ["Dictionary: <{}>".format(id(dict))]
    _str.append("".join(["-" for _ in range(len(_str[0]))]))
    for c, d in enumerate(dic.keys()):
        _str.append("{}|({})|{}".format("".join(["0" for x in range(floor(len(dic.keys())/10)-1)])+str(c), d, dic[d] if len(str(dic[d])) < 60 else str(dic[d])[:60]+"...")) 
    print("\n".join(_str))
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
        @self.app.route("/point")
        def nPoint():
            print("Creating Point")
            self.objects.append(Point_Cloud.from_dict(request.json).as_dict())
            dict_to_table(Point_Cloud.from_dict(request.json).as_dict())
            self.socketio.emit("point", Point_Cloud.from_dict(request.json).as_dict())
            return self.objects
        @self.app.route("/box")
        def nBox():
            print("Creating Box")
            box = Box.from_dict(request.json)
            self.objects.append(box.as_dict())
            self.socketio.emit("box", box.as_dict())
            return box.as_dict()
        
        @self.app.route("/remove")
        def nRemove():
            print("Removing Object")
            dic = dict(request.json)
            for c, i in enumerate(self.objects):
                if i["uuid"] == dic["uuid"]:
                    print("Found Element")
                    self.objects.pop(c)
                    self.socketio.emit(dic["type"], {
                        "uuid":dic["uuid"],
                        "event": "remove"
                    })
                    return self.objects
            raise IndexError("The Provided UUID has no index in python array")
        
        @self.app.route("/move")
        def nMove():
            print("Moving Object")
            dic = dict(request.json)
            for c, i in enumerate(self.objects):
                if i["uuid"] == dic["uuid"]:
                    print(self.objects[c])
                    self.objects[c]["position"] = dic["position"]
                    self.socketio.emit(dic["type"], {
                        "uuid":dic["uuid"],
                        "position":dic["position"],
                        "event": "move"
                    })
                    return self.objects
            raise IndexError("The Provided UUID has no index in python array")

        @self.app.route("/objects")
        def all_objects():
            uuid_only = bool(request.args.get("uuid_only"))
            self.socketio.emit("objects", {})
            if uuid_only:
                print("UUID")
                return [
                    item["uuid"] for item in self.objects
                ]
            else:
                return self.objects
 
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
