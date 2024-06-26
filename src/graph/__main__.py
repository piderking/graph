from flask import Flask, Request, Response, render_template, url_for, request
from flask_socketio import SocketIO, send,emit
from uuid import uuid4
from typing import Type
from math import floor
from graph.shapes import Shape, Point_Cloud, Box
import json
from time import time
import os
import logging
from logging import info, warn

logging.basicConfig(filename='graph.log', encoding='utf-8', level=logging.DEBUG)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def dict_to_table(dic: dict) -> None:
    """Visual Representation

    Args:
        dic (dict): dictionary to be viewd
    """
    _str = ["Dictionary: <{}>".format(id(dict))]
    _str.append("".join(["-" for _ in range(len(_str[0]))]))
    for c, d in enumerate(dic.keys()):
        _str.append("{}|({})|{}".format("".join(["0" for x in range(floor(len(dic.keys())/10)-1)])+str(c), d, dic[d] if len(str(dic[d])) < 60 else str(dic[d])[:60]+"...")) 
    info("Dictionary to Table: \n"+"\n".join(_str))
class Data:

    def __init__(self, sync_db = True, fPath:str = os.path.join(os.path.abspath("."), "db.json")) -> None:


        self.app = Flask(__name__, 
            static_url_path='', 
            static_folder='assets/static',
            template_folder='assets/templates'
        )
        info("Running from directory: {}".format(os.getcwd()))
        
        self.app.wsgi_app = AuthorizationMiddleWare(self.app.wsgi_app, self)
        self.app.config['SECRET_KEY'] = str(uuid4())
        self.socketio = SocketIO(self.app)
        self.fPath = fPath


        self._objects = [
            
        ]

        
        # Clients (Web Pages)
        self.clients = [

        ]
        # APIs
        self.api = [
            {
                "id":"admin",
                "passkey":"admin",
                "code":"admin",
                "actions":[]
            }
        ]

        if sync_db and os.path.exists(fPath):
            jso: dict = json.load(open(fPath, "r"))
            self._objects = jso.get("objects") if not jso.get("objects") is None else self.objects 
            self.clients = jso.get("clients") if not jso.get("clients") is None else self.clients  
            self.api = jso.get("api") if not jso.get("api") is None else self.objects   
        else:
            if not os.path.exists(fPath): open(fPath, "w").write("{}")
        # Methods Define
        @self.app.route("/", methods=["GET"])
        def home():
            """List Methods and Static Files
            """
            def list_dir(path) -> list:
                _r = []
                for item in os.scandir(path):
                    if item.is_dir():
                        _r.append({
                            "folder":item.name,
                            "contents": list_dir(item.path)
                            
                        })
                    else:
                        _r.append(os.path.relpath(item.path).replace("\\", "/").removeprefix("src/graph/assets"))
                return _r
            
            links = {}
            dirs = []
            for rule in self.app.url_map.iter_rules():
                # Filter out rules we can't navigate to in a browser
                # and rules that require parameters
                if has_no_empty_params(rule):
                    url = url_for(rule.endpoint, **(rule.defaults or {}))
                    links[rule.endpoint] = {
                        "url": url,
                        "endpoint": rule.endpoint,
                        "doc": self.app.view_functions[rule.endpoint].__doc__.strip() if not self.app.view_functions[rule.endpoint].__doc__ is None else None,
                        "methods": list(rule.methods),
                    }
            return {

                "links":links,
                "static": list_dir(os.path.join(os.path.abspath("."), "src", "graph", "assets"))
            }

        @self.app.route("/status", methods=["GET"])
        def status():
            """Initialize API"""
            uid = str(request.json["id"])
            passkey = str(request.json["passkey"])
            for i, api_user in enumerate(self.api):
                if api_user["id"] == uid:
                    if api_user["passkey"] == passkey:
                        info("Previously Connected API User Join!")
                        if not api_user.get("code") is None:
                            
                            return {
                                "message": "Good!",
                                "actions": "\n".join(api_user["actions"]),
                                "code":api_user["code"]
                            }, 200
                        else:
                            code = str(uuid4())
                            self.api[i] = {
                                "id": api_user["id"],
                                "passkey": api_user["passkey"],
                                "actions": api_user["actions"],
                                "code": code
                            }
                            return {
                                "message": "Good!",
                                "actions": "\n".join(api_user.actions),
                                "code":code
                            }, 200
                    else:
                        info("Previously Connected API User Failed to input correct passkey")

                        return {
                            "message": "Passkey Incorrect!",
                        }, 400
            if bool(request.json["create"]) == True:
                code = str(uuid4())

                self.api.append({
                    "id":uid,
                    "passkey":passkey,
                    "code":code,
                    "actions":[]
                })
                return {
                            "message": "Created!",
                            "actions": "",
                            "code":code
                        }, 200
            else:
                return {
                            "message": "Not Account exsist and didn't want to create one!",
                            "actions": ""
                        }, 300


        @self.app.route('/client', methods=["GET"])
        def client():
            return render_template("index.html")
        

        
        @self.socketio.on('connect')
        def connection():
            info("Client Connected with SID of {}".format(request.sid))
        @self.socketio.on('init')
        def start(data):
            _id = str(request.sid)
            self.clients.append({
                "id": _id, 
            })
            info("Client ({}) requests to initalize and sync".format(_id))
            emit("text", {"text": "Syncing", "time":1000})
            emit("sync", {
                "len": 10,
                "sid": _id,
                "objects": self.objects
            }, to=_id)
            info("Client ({}) finished sync".format(_id))
        
        @self.socketio.on("disconnect")
        def disconnect():
            for i, client in enumerate(self.clients):
                if client["id"] == request.sid:
                    self.clients.pop(i)
                    return
            raise Warning("User with SID: {} not found in clients connected list -- disconnect".format(request.sid))


        @self.app.route("/point", methods=["GET"])
        def nPoint():
            try:
                _point = Point_Cloud.from_dict(request.json).as_dict()
                info("Point Event: {}".format(_point["event"]))
                self.objects.append(_point)
                dict_to_table(_point)
                self.socketio.emit("point", _point)
                return _point
            except Exception as e:
                return {
                    "reason":"e"
                }
        @self.app.route("/point/<uuid>", methods=["GET"])
        def nPoint_look_up(uuid):
            info("Looking up Point Cloud")
            for _object in self.objects:
                if _object["uuid"] == uuid:
                    return _object, 200
                    
                else:
                    return {"message": "Point Cloud with uuid was not found"}, 404
                          
        @self.app.route("/box", methods=["POST"])
        def nBox():
            # NOTE This doesn't work as intended right now TODO Fix Box? or Deprecate
            box = Box.from_dict(request.json)
            self.objects.append(box.as_dict())
            self.socketio.emit("box", box.as_dict())
            return box.as_dict()
        
        @self.app.route("/remove")
        def nRemove():
            raise DeprecationWarning("Use /point instead")
            info("Removing Object")
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
            raise DeprecationWarning("Use /point instead")
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
                    return Response(self.objects, status=200)
            return Response({
                "exsists":False
            })  

        @self.app.route("/objects", methods=["GET"])
        def all_objects():
            # /object or /object?uuid_only=true
            uuid_only = bool(request.args.get("uuid_only"))
            self.socketio.emit("objects", {})
            if uuid_only:
                return [
                    item["uuid"] for item in self.objects
                ]
            else:
                return self.objects
        
        @self.app.route("/apis", methods=["GET"])
        def all_apis():
            return {
                "apis": [
                    {
                        "id":api["id"],
                        "actions":"\n".join(api["actions"])
                    } for api in self.api
                ], "number": len(self.api)
            }
        
        @self.app.route("/clients", methods=["GET"])
        def all_clients():
            return {
                "clients": [
                   clients for clients in self.clients
                ], "number": len(self.clients)
            }
        @self.app.route('/save', methods=["GET"])
        def save():
            self.saveToFile()
            return self._objects

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
    def addAction(self, uid: str, action: str):
        for i, api_user in enumerate(self.api):
            if api_user["id"] == uid:
                self.api[i]["actions"].append(action)
    def run(self):
        while True:
            try:
                d.socketio.run(d.app,debug=True)
            except KeyboardInterrupt:
                d.saveToFile()
    def saveToFile(self):
        open(self.fPath, "w").write(json.dumps(
            {
                "objects": self._objects,
                "clients": self.clients,
                "api": self.api
            }
        ))

class AuthorizationMiddleWare():
    '''
    Simple WSGI middleware
    '''

    def __init__(self, app, data: Data):
        self.app = app
        self.data = data
        self.un_authorized = [
            #"point" # Disabled temporarily for testing
        ]


    def __call__(self, environ, start_response):
        _request = Request(environ)
        if not _request.url.split("/")[-1].strip().lower() in self.un_authorized:
            return self.app(environ, start_response)
        try:
            header = json.loads(_request.headers.get("Authorization"))
            uid = header.get("id")
            code = header.get("code")

            if uid == None or code == None:
                info("{}:{} failed credentials".format(str(uid), str(code)))

                raise Exception("Missing Credentials!")
            
            for api_user in self.data.api:
                if api_user["id"] == uid and api_user["code"] == code:
                    return self.app(environ, start_response)
            raise Exception("No User Found!")
        
        except Exception as e:
            # print("Authorization Failed ;(" + str(e))
            res = Response(u'Authorization failed:{}'.format(str(e)), mimetype= 'text/plain', status=401)
            return res(environ, start_response)  
        



    
if __name__ == '__main__':
    d = Data()
    #d.objects = Box({"x":1,"y":1,"z":1}, {"x":1,"y":1,"z":1},9009)
    #d.objects = Box({"x":1,"y":1,"z":1}, {"x":2,"y":1,"z":1},9009)
    d.run()