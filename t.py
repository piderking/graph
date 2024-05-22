from graph import Graph
import numpy as np 
from math import cos, sin, pi

d = Graph("http://127.0.0.1:5000/")
# data: np.ndarray,scale: int,size: int,position: dict,color: str
# uuid = d.graph(np.array([x for x in range(36)]), 1, 1, {"x":1,"y":1,"z":1}, 9111,)

uuid2 = d.graph(np.array([sin(2 * pi * x / 3 / 12) if x % 3 == 0 else 0 for x in range(36)]), {"x":1,"y":1,"z":1}, .1, {"x":1,"y":1,"z":1}, 3404)


# d.moveObject(uuid2, "point", 1.0, 0, 0)
print(uuid2)

#
# d.removeObject(uuid, "point")