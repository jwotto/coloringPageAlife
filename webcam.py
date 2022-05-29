
import cv2 as cv
import numpy as np
import copy

last_biggest = None

def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv.contourArea(i)
        if area > 100:
            peri = cv.arcLength(i, True)
            approx = cv.approxPolyDP(i, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
                print(area)

    return biggest


video = cv.VideoCapture(1)

while True:
    ret, frame = video.read()
  

    img_original = frame.copy()

    # Image modification
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.bilateralFilter(gray, 20, 30, 30)
    edged = cv.Canny(gray, 10, 20)
    
    # Contour detection
    contours, hierarchy = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)[:10]

    biggest = biggest_contour(contours)

    #if contour is detected
    if biggest.all() > 1:
        print(biggest)
        cv.drawContours(frame, [biggest], -1, (255, 0, 0), 7)
   
        
  
    
    cv.circle(frame, (500, 200), 100, (255,0,0), 7)
  
    cv.imshow("Contour detection", frame)

    
    
    
    
    if cv.waitKey(500) == ord('x'): 
        break


video.release()
cv.destroyAllWindows()