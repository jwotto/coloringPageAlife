import cv2 as cv
import matplotlib.pyplot as plt #usefull for working with images


#IMREAD_GRAYSCALE for black and white
img = cv.imread("Photos/cat.png",cv.IMREAD_COLOR)

#cv.imshow("cat",img)

plt.imshow(img)
plt.show()

cv.waitKey(0)
cv.destroyAllWindows()
