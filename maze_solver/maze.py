from maze_solver.helpers import Vertex
import numpy as np
import heapq
import cv2

class Maze:
    def __init__(self, bgr_img, is_augmented=False):
        """
        Args:
            bgr_img (numpy matrix): Img matrix (bgr) read from cv2.imread. Can
                                    be original maze img or augmented with
                                    thick lines.
        """
        self.__img = bgr_img
        self.__is_augmented = is_augmented
        self.__row_size = bgr_img.shape[1]
        self.__col_size = bgr_img.shape[0]

        self.__path = []
        self.__start = ()
        self.__end = ()

        self.__mat = np.full((self.__row_size,self.__col_size), None)
        

    def get_shortest_path(self, start, end):
        """Get shortest connecting path using Dijkstra's Algorithm

        Args:
            start (tuple of int): (x,y) coordinate of start location
            end (tuple of int): (x,y) coordinate of end location

        Returns:
            list of tuples: Pixels (x,y) joining the path from start to end
        """
        self.__reset_vertex_matrix()

        '''Below code fixes bug that arises due to augmentation of Maze
        img to get clear path from start to end. Due to augmentation, the start
        and end pixel rgb values may change from (255,255,255) to (0,0,0) and
        consequently a wrong path through maze boundaries may be calculated.
        '''
        if self.__is_augmented:
            strt = (start[1],start[0])
            stop = (end[1],end[0])

            self.__img[strt] = [255, 255, 255]
            self.__img[stop] = [255, 255, 255]

        self.__start = start
        self.__end = end
        start_x, start_y = start[0], start[1]
        end_x, end_y = end[0], end[1]

        self.__mat[start_x][start_y].dist = 0

        pq = [self.__mat[start_x][start_y]]
        
        while(len(pq) > 0):
            # Get the next least distanced node
            node = heapq.heappop(pq)

            # Nodes can get added to the priority queue multiple times. We only
            # process a vertex the first time we remove it from the 
            # priority queue.
            if node.dist > self.__mat[node.x][node.y].dist:
                continue

            neighbours = self.__get_neighbours(node.x, node.y)

            for n_node in neighbours:
                new_dist = node.dist + self.__get_distance((node.y,node.x), 
                                                        (n_node.y,n_node.x))
                
                # Only consider this new path if it's better than any path 
                # we've already found.
                if new_dist < self.__mat[n_node.x][n_node.y].dist :
                    self.__mat[n_node.x][n_node.y].dist = new_dist
                    self.__mat[n_node.x][n_node.y].parent_x = node.x
                    self.__mat[n_node.x][n_node.y].parent_y = node.y

                    heapq.heappush(pq, self.__mat[n_node.x][n_node.y])


        path = [(end_x, end_y)]
        iter_v = self.__mat[end_x][end_y]
        while (iter_v.x, iter_v.y) != (start_x, start_y):
            path.append((iter_v.parent_x, iter_v.parent_y))
            iter_v = self.__mat[iter_v.parent_x][iter_v.parent_y]

        path.reverse()
        self.__path = path
        return path

    def __reset_vertex_matrix(self):
        """Reset the pixel vertex matrix
        """
        for row in range(self.__row_size):
            for col in range(self.__col_size):
                self.__mat[row][col] = Vertex(row, col)

    def __get_neighbours(self, row, col):
        """Get the adjacent neighbours of a pixel

        Args:
            row (int): x coordinate of the pixel
            col (int): y coordinate of the pixel

        Returns:
            list of Vertex: Neighbours of pixel at (row,col)
        """
        neighbours = []

        if row > 0:
            neighbours.append(self.__mat[row-1][col])
        if row < (self.__row_size-1) :
            neighbours.append(self.__mat[row+1][col])
        if col > 0 :
            neighbours.append(self.__mat[row][col-1])
        if col < (self.__col_size-1):
                neighbours.append(self.__mat[row][col+1])
        return neighbours

    def __get_distance(self,u,v):
        """Get distance between two pixels

        Args:
            u (tuple(int)): (y,x) coordinate of pixel u
            v (tuple(int)): (y,x) coordinate of pixel v

        Returns:
            distance (float): Distance between the pixels
        """
        dist = 0.1 \
                + (float(self.__img[v][0])-float(self.__img[u][0]))**2 \
                + (float(self.__img[v][1])-float(self.__img[u][1]))**2 \
                + (float(self.__img[v][2])-float(self.__img[u][2]))**2
        return dist

    def get_solution_image(self, alt_img=None, line_color=(255,0,0), 
                            line_width=2):
        """Get image with path maze path drawn over it

        Args:
            alt_img (np.mat, optional): An alternate maze image, used to draw 
            over the solution if augmented img was used to find the path.
            Defaults to None.
            line_color (tuple, optional): [description]. Defaults to (255,0,0).
            line_width (int, optional): [description]. Defaults to 2.

        Returns:
            [type]: [description]
        """
        x0, y0 = self.__path[0]
        if alt_img is None:
            sol_img = np.copy(self.__img)
        else:
            sol_img = np.copy(alt_img)

        for vertex in self.__path[1:]:
            x1,y1=vertex
            cv2.line(sol_img,(x0,y0),(x1,y1),line_color,line_width)
            x0,y0=vertex

        cv2.circle(sol_img, self.__start, radius=3, 
                color=(0,255,0), thickness=-1)
        cv2.circle(sol_img, self.__end, radius=3, 
                color=(0,0,255), thickness=-1)
        
        return sol_img


