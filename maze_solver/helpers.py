class Vertex:
    def __init__(self,x_coord,y_coord):
        self.x=x_coord
        self.y=y_coord
        self.dist=float('inf') #distance from source
        self.parent_x=-1
        self.parent_y=-1

    def __lt__(self, other):
        return self.dist < other.dist