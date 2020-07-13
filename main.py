"""This script lets you choose any maze img, whose path given as
commandline argument, and draw the path between chosen start and end point.
Usage:
    python main.py [path to maze image]
    Click on maze image to set start and end points and press enter to
    generate the corresponding path.
    If clicked on a point unintentionally, press 'r' key to reset start and
    end points.
    To quit the program, press 'q' key.
    """
import cv2
import os
import sys
from maze_solver.maze import Maze
from maze_augmenter.img_handler import ImgMaze

ENTER_KEY = 13
click_number = 0
start = ()
end = ()

def mouse_callback(event, x, y, flags, param):
    global click_number
    global start
    global end
    if event == cv2.EVENT_LBUTTONDOWN:
        if click_number is 0:
            start = (x, y)
            print(f"start: ({x},{y})")
            click_number = 1
        else:
            end = (x, y)
            print(f"end: ({x},{y})")
            click_number = 0
        
def main():
    if len(sys.argv) is not 2:
        print("Error: Please provide path to maze image!!")
        exit(1)

    global start, end, click_number
    img_path = sys.argv[1]
    img_path = os.path.abspath(img_path)

    img_obj = ImgMaze(img_path)
    maze_orig = img_obj.get_bgr_maze()
    maze_aug = img_obj.get_augmented_bgr_maze()

    cv2.namedWindow('Maze image')
    cv2.setMouseCallback('Maze image', mouse_callback)

    while True:
        cv2.imshow('Maze image', maze_orig)
        key = cv2.waitKey(0) & 0xFF

        if(key == ord('r')):
            click_number = 0
            start = ()
            end = ()
            continue

        elif(key == ENTER_KEY):
            sol_obj = Maze(maze_aug, is_augmented=True)
            sol_obj.get_shortest_path(start, end)
            sol_img1 = sol_obj.get_solution_image(alt_img=maze_orig, 
                                                    line_width=2)
            cv2.imshow('Solution', sol_img1)
            cv2.waitKey(0)
            cv2.destroyWindow('Solution')

        elif(key == ord('q')):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
                        

