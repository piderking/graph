# Display Point Clouds! 
Create 3D Points Clouds with built in support for mediapipe

### How to Run
- Clone Repository
```bash
git clone https://github.com/piderking/graph.git graph
```
- Install library ```pip3 install -e graph```
- Run ```python -m graph``` to start server

### Usage
```python 
from graph import Graph
from graph.shapes import Point_Cloud
obj = Point_Cloud(
        "http://127.0.0.1:5000/", # URL the server is running on
        np.array([math.floor(x/3) for x in range(63)]), # Ramge is group of Vector3
        lines=False, # Only for mediapipe data
        size=.1, # Size of the point
        connections=[[4, 20, 10, 9001]] # First two values are index in the array passed

    )
    uuid2 = d.graph(obj)
```
### Mediapipe Usage
- See other repository [Keyboard]()

### Contact