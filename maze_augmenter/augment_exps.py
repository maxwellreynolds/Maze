import cv2
import numpy as np


test_img = '../maze.png'

def output_hough_lines(img_bgr, minLineLength, maxLineGap, threshold):
    img = np.copy(img_bgr)
    gray_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.bitwise_not(gray_img)
    edges = cv2.Canny(gray_img, 50, 150)
    lines = cv2.HoughLinesP(image=edges,
                            rho=1,
                            theta=np.pi/180,
                            threshold=threshold,
                            minLineLength=minLineLength,
                            maxLineGap=maxLineGap)
    try:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 4)
    except:
        pass
    return img
    


def main():
    img = cv2.imread(test_img)

    minLineLength = 1
    maxLineGap = 1
    hough_threshold = 2
    
    hlines_img = output_hough_lines(img, minLineLength, 
                                    maxLineGap, hough_threshold)
    
    edges = edges = cv2.Canny(img,50,150)
    kernel = np.ones((5,5), np.uint8)

    img_erosion = cv2.erode(hlines_img, kernel, iterations=2) 
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=2) 

    cv2.imshow('original', img)
    cv2.imshow('hough', hlines_img)
    cv2.imshow('morphed', img_dilation)
    # cv2.imshow('canny', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()