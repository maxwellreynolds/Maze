import cv2
# from maze import Maze
from maze import Maze


maze_image = '../maze.png'

start = (9,12)
end = (213,211)

test = True

test_img = cv2.imread(maze_image)
if test:
    maze_solver = Maze(test_img)
    maze_solver.get_shortest_path(start=start, end=end)

    test_img = maze_solver.get_solution_image()

cv2.imshow('image',test_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
