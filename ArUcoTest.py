import os
import cv2 as cv
import cv2.aruco as aruco
import numpy as np
import os


def main():
    video = cv.VideoCapture(1)
    while True:
        ret, frame = video.read()
        cv.imshow("cam", frame)
        if cv.waitKey(30) == ord('x'): 
            break
                

    video.release()
    cv.destroyAllWindows()
