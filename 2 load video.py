import cv2 as cv
video = cv.VideoCapture(0)

while True:
    ret, frame = video.read()
    if ret:
        cv.imshow("beat", frame)
        if cv.waitKey(30) == ord('x'): 
            break
    else:
        video = cv.VideoCapture("Photos/dance.mov")

    
video.release()
cv.destroyAllWindows()