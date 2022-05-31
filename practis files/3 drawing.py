import cv2 as cv
import matplotlib.pyplot as plt #usefull for working with images


#IMREAD_GRAYSCALE for black and white
img = cv.imread("Photos/cat.png",cv.IMREAD_COLOR)



cv.rectangle(img, (350,450), (500,350), (0,255,0), 5)
cv.circle(img, (500, 200), 100, (255,0,0), 7)

cv.imshow("cat",img)



 

cv.waitKey(0)
cv.destroyAllWindows()