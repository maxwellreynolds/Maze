import streamlit as st
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import maze


st.title('Maze Solver')
uploaded_file = st.file_uploader("Choose an image", ["jpg","jpeg","png"])
opencv_image = None

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    st.image(opencv_image, channels="BGR", width=800)

if opencv_image is not None:
    start_x = st.slider("Start X", value=50, min_value=0, max_value=opencv_image.shape[1], key='sx')
    start_y = st.slider("Start Y", value=100, min_value=0, max_value=opencv_image.shape[0], key='sy')
    finish_x = st.slider("Finish X", value=100, min_value=0, max_value=opencv_image.shape[1], key='fx')
    finish_y = st.slider("Finish Y", value=100, min_value=0, max_value=opencv_image.shape[0], key='fy')

markedup_image = None

if opencv_image is not None:
    markedup_image = opencv_image.copy()
    circle_thickness=(markedup_image.shape[0]+markedup_image.shape[0])//2//100
    cv2.circle(markedup_image, (start_x, start_y), circle_thickness, (0,255,0),-1)
    cv2.circle(markedup_image, (finish_x, finish_y), circle_thickness, (255,0,0),-1)
    st.image(markedup_image, channels="RGB", width=800)

if markedup_image is not None:
    if st.button('Solve Maze'):
        st.write('Solving your maze, image will display below when done')
        path = maze.find_shortest_path(opencv_image,(start_x, start_y),(finish_x, finish_y))
        pathed_image = opencv_image.copy()
        path_thickness = (pathed_image.shape[0]+pathed_image.shape[0])//2//100
        maze.drawPath(pathed_image, path, path_thickness)
        st.image(pathed_image, channels="RGB", width=800)
    else:
        st.write('Solved maze will be shown here')