
import cv2 as cv
import numpy as np
import imutils

path = 'Photos/cat.png'

image = cv.imread(path)

window_name = 'image'
  

#cv.imshow(window_name, image)

rotated = imutils.rotate(image, 5)
cv.imshow("Rotated by 180 Degrees", rotated)
#cv.getRotationMatrix2D(0,0,40)


cv.waitKey(0) 
cv.destroyAllWindows() 
