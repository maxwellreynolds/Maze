import streamlit as st
import cv2
import matplotlib.pyplot as plt
import numpy as np

from maze_augmenter.img_handler import ImgMaze
from maze_solver.maze import Maze

def main():

    st.title('Maze Path Planner')
    uploaded_file = st.file_uploader("Choose an image", ["jpg","jpeg","png"])
    st.write('Or')
    use_default_image = st.checkbox('Use default maze')
    maze_image = None
    maze_aug_image = None
    marked_image = None

    if use_default_image:
        maze_img_obj = ImgMaze('maze.png', is_filebytes=False)
        maze_image = maze_img_obj.get_bgr_maze()
        maze_aug_image = maze_img_obj.get_augmented_bgr_maze()

    elif uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        maze_img_obj = ImgMaze(file_bytes, is_filebytes=True)
        maze_image = maze_img_obj.get_bgr_maze()
        maze_aug_image = maze_img_obj.get_augmented_bgr_maze()

    if maze_image is not None:
        st.subheader('Use the sliders on the left to position the start and end points')
        start_x = st.sidebar.slider("Start X", value= 8 if use_default_image  else 50, min_value=0, max_value=maze_image.shape[1], key='sx')
        start_y = st.sidebar.slider("Start Y", value= 9 if use_default_image  else 100, min_value=0, max_value=maze_image.shape[0], key='sy')
        finish_x = st.sidebar.slider("Finish X", value= 216 if use_default_image  else 100, min_value=0, max_value=maze_image.shape[1], key='fx')
        finish_y = st.sidebar.slider("Finish Y", value= 216 if use_default_image  else 100, min_value=0, max_value=maze_image.shape[0], key='fy')
        marked_image = maze_image.copy()
        circle_thickness=(marked_image.shape[0]+marked_image.shape[0])//2//100 #ui circle thickness based on img size
        cv2.circle(marked_image, (start_x, start_y), circle_thickness, (0,255,0),-1)
        cv2.circle(marked_image, (finish_x, finish_y), circle_thickness, (255,0,0),-1)
        st.image(marked_image, channels="RGB", width=800)

    if marked_image is not None:
        if st.button('Get Path'):
            with st.spinner('Searching for path from start to end'):
                maze_solver_obj = Maze(maze_aug_image, is_augmented=True)
                maze_solver_obj.get_shortest_path(start=(start_x, start_y), 
                                                end=(finish_x, finish_y))
            
            path_thickness = (maze_image.shape[0]+maze_image.shape[0])//2//100
            maze_sol_image = maze_solver_obj.get_solution_image(
                                                alt_img=maze_image, 
                                                line_width=path_thickness)
            
            st.image(maze_sol_image, channels="RGB", width=800)

if __name__ == "__main__":
    main()