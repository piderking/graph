from graph import Graph
import numpy as np 

d = Graph("http://127.0.0.1:5000/")
# data: np.ndarray,scale: int,size: int,position: dict,color: str
uuid = d.graph(np.array([x for x in range(36)]), 1, 1, {"x":1,"y":1,"z":1}, 9111,)
uuid2 = d.graph(np.array([x+1 for x in range(36)]), 1, 1, {"x":1,"y":1,"z":1}, 1000,)


d.moveObject(uuid, "point", 1.0, 0, 0)
print(uuid)

#
# d.removeObject(uuid, "point")