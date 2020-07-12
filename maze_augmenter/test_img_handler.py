from img_handler import ImgMaze
import cv2
test_img = '../maze.png'

maze_obj = ImgMaze(test_img)
maze_bgr = maze_obj.get_bgr_maze()
maze_gray = maze_obj.get_gray_maze()
maze_inv_gray = maze_obj.get_inv_gray_maze()
maze_aug = maze_obj.get_augmented_bgr_maze()

cv2.imshow('color',maze_bgr)
# cv2.imshow('gray', maze_gray)
# cv2.imshow('inverted_gray', maze_inv_gray)
cv2.imshow('augmented', maze_aug)

cv2.waitKey(0)
cv2.destroyAllWindows()