import cv2 as cv
import numpy as np
video = cv.VideoCapture(0)



while True:
    ret, frame = video.read()
  
    cv.imshow("cam", frame)
    if cv.waitKey(30) == ord('x'): 
        break



video.release()
cv.destroyAllWindows()