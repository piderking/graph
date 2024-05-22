from graph import Graph
import numpy as np 
from math import cos, sin, pi

d = Graph("http://127.0.0.1:5000/")
# data: np.ndarray,scale: int,size: int,position: dict,color: str
# uuid = d.graph(np.array([x for x in range(36)]), 1, 1, {"x":1,"y":1,"z":1}, 9111,)

uuid2 = d.graph(np.array([x/2 if x % 3 == 0 else (c-1)/3 if (x%3)-1 == 0 else (c-2)/3 for c, x in enumerate(range(63))]), {"x":1,"y":1,"z":1}, .1, {"x":0,"y":0,"z":0}, 3404, True, True)


d.moveObject(uuid2, "point", 1.0, 0, 0)
print(uuid2)

#
# d.removeObject(uuid, "point")