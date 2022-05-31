import cv2 as cv
video = cv.VideoCapture(1)
fourcc = cv.VideoWriter_fourcc(*'XVID')
writer = cv.VideoWriter('video.avi',fourcc,60.0,(640,480))



while True:
    ret, frame = video.read()  
    cv.imshow("cam", frame)
    if cv.waitKey(30) == ord('x'): 
        break


video.release()
writer.release()
cv.destroyAllWindows()

 

