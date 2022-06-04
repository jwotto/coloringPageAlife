import os
import cv2 as cv
import cv2.aruco as aruco
import numpy as np
import os
import time

camera = 0
cameraWidth = 1920
cameraHeight = 1080

def main():
    video = cv.VideoCapture(camera)
    video.set(3, cameraWidth)
    video.set(4, cameraHeight)
    time.sleep(2)


    while True:
        ret, frame = video.read()
        cv.imshow("cam", frame)
        if cv.waitKey(30) == ord('x'): 
            break
                

    video.release()
    cv.destroyAllWindows()


main()
