from re import X
import cv2 as cv

img1 = cv.imread('Photos/laptop.png')
img2 = cv.imread('Photos/logo.png')

logo_gray = cv.cvtColor(img2, cv.COLOR_RGB2GRAY)
ret, mask = cv.threshold(logo_gray, 180, 255, cv.THRESH_BINARY_INV)

#inverts picture
mask_inv = cv.bitwise_not(mask)

rows, columns,channels = img2.shape
area = img1[0:rows,0:columns]

img1_bg = cv.bitwise_and(area, area, mask=mask_inv)
img2_fg = cv.bitwise_and(img2, img2, mask=mask)
 
img1_bg = cv.bitwise_and(area, area, mask=mask_inv)
img2_fg = cv.bitwise_and(img2, img2, mask=mask)

 


cv.imshow("output",img1)



cv.waitKey(0)
cv.destroyAllWindows()
