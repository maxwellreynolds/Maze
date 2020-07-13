import cv2
import os
from maze_solver.maze import Maze
from maze_augmenter.img_handler import ImgMaze

# test_img = './maze.png'
# start = (9,12)
# end = (213,211)

test_img = './Maze_1.png'
start = (8,10)
# end = (588,591)
# end = (369,354)
end = (592,9)
# end = (7,591)

test_img = os.path.abspath(test_img)

maze_obj = ImgMaze(test_img)
orig_img = maze_obj.get_bgr_maze()
aug_img = maze_obj.get_augmented_bgr_maze()

sol_obj = Maze(aug_img, is_augmented=True)
sol_obj.get_shortest_path(start, end)
sol_img1 = sol_obj.get_solution_image(alt_img=orig_img, line_width=2)

# sol_obj2=Maze(orig_img)
# sol_obj2.get_shortest_path(start, end)
# sol_img2 = sol_obj2.get_solution_image(line_width=2)

cv2.imshow('Original Maze', orig_img)
cv2.imshow('Augmented Maze', aug_img)
# cv2.imshow('Normal Solution', sol_img2)
cv2.imshow('New Solution', sol_img1)

cv2.waitKey(0)
cv2.destroyAllWindows()