import cv2 as cv
import numpy as np
video = cv.VideoCapture(1)

cv.circle(video, (500, 200), 100, (255,0,0), 7)

while True:
    ret, frame = video.read()
  
    cv.imshow("cam", frame)
    if cv.waitKey(1) == ord('x'): 
        break



video.release()
cv.destroyAllWindows()