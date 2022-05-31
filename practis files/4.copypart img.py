import cv2 as cv
import matplotlib.pyplot as plt #usefull for working with images


#IMREAD_GRAYSCALE for black and white
img = cv.imread("Photos/cat.png",cv.IMREAD_COLOR)

copypart = img[300:500,300:700]
img[100:300,100:500] = copypart
#img[300:500,300:700]=[0,0,0]

cv.imshow("cat",img)


cv.waitKey(0)
cv.destroyAllWindows()
