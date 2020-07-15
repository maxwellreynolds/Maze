import cv2

maze_path = 'maze5.jpg'
img = cv2.imread(maze_path)
print('img_shape', img.shape)
cv2.imshow('Maze', img)
cv2.waitKey(0)
cv2.destroyAllWindows()