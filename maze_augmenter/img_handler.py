import cv2
import numpy as np

# First set of Hough, Canny etc parameter values for augmentation
HOUGH_MINLINELENGTH = 1
HOUGH_MAXLINEGAP = 1
HOUGH_THRESHOLD = 2
CANNY_THRESHOLD1 = 50
CANNY_THRESHOLD2 = 150
LINE_COLOR = (0,0,0)
LINE_THICKNESS = 3
MORPH_KERNEL_SIZE = 3
EROSION_ITER = 3
DILATION_ITER = 1

class ImgMaze:
    def __init__(self, img_path, is_filebytes):
        """Constructor for ImgMaze class

        Args:
            img_path (str): Path of image file
            is_filebytes (bool): Whether arg{img_path} is a filebytes or string
        """
        self.__img = img_path
        self.__is_filebytes = is_filebytes
        if is_filebytes:
            self.__readimage = cv2.imdecode
        else:
            self.__readimage = cv2.imread
            

    def get_bgr_maze(self):
        return self.__readimage(self.__img, flags=cv2.IMREAD_COLOR)

    def get_gray_maze(self):
        return self.__readimage(self.__img, flags=cv2.IMREAD_GRAYSCALE)

    def get_inv_gray_maze(self):
        gray_img = self.__readimage(self.__img, flags=cv2.IMREAD_GRAYSCALE)
        inv_gray = cv2.bitwise_not(gray_img)
        return inv_gray

    def get_augmented_bgr_maze(self):
        img = self.__get_maze_with_hlines(
                            minLineLength=HOUGH_MINLINELENGTH,
                            maxLineGap=HOUGH_MAXLINEGAP,
                            threshold=HOUGH_THRESHOLD,
                            line_color=LINE_COLOR,
                            line_thickness=LINE_THICKNESS)

        k_size = MORPH_KERNEL_SIZE
        kernel = np.ones((k_size,k_size), np.uint8)

        eroded_img = cv2.erode(img, kernel, iterations=EROSION_ITER) 
        aug_img = cv2.dilate(eroded_img, kernel, iterations=DILATION_ITER)
        return aug_img

    def __get_maze_with_hlines(self, minLineLength, maxLineGap, threshold, 
                                line_color, line_thickness):
        img_bgr = self.get_bgr_maze()
        gray_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        gray_img = cv2.bitwise_not(gray_img)
        edges = cv2.Canny(gray_img, CANNY_THRESHOLD1, CANNY_THRESHOLD2)
        lines = cv2.HoughLinesP(image=edges,
                                rho=1,
                                theta=np.pi/180,
                                threshold=threshold,
                                minLineLength=minLineLength,
                                maxLineGap=maxLineGap)
        try:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img_bgr, (x1, y1), (x2, y2), 
                    line_color, line_thickness)
        except:
            print("ImgMaze->__get_maze_with_hlines: Unknown error")
        return img_bgr


    
