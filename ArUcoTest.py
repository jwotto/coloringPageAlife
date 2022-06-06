from pickle import FALSE, TRUE
import cv2 as cv
from pandas import array
import cv2.aruco as aruco
import numpy as np
import time

#camera setup
camera = 1
cameraWidth = 1280
cameraHeight = 720
frameRate = 30

#colering pages lis
colleringPageName = ['Gebouw','Raam',]

cornersPage = [(0,0),(0,0),(0,0),(0,0)] # [leftTop,rightTop,rightBottom,leftBottom]

frameRate = int(1000/frameRate)

#returns the group id dor example id 0 to 3 is group 0 and id 4 to 7 is group 1
def groupId(id):
    id = (id - (id%4)) /4
    return int(id)

#are there 4 unique codes with the same group id?
def uniqueIdCornerCheck(idList):
    idSum = 0 
    if len(idList) == 4:
        for i in range(4):   
            idSum += ((idList[i]%4)+1)
        if idSum == 10: # because 1+2+3+4 = 10
            return True
        else: 
            return False
    else:
        return False


def main():
    # set video capture
    video = cv.VideoCapture(camera)
    video.set(3, cameraWidth)
    video.set(4, cameraHeight)

    # Load Aruco detectorx
    parameters = cv.aruco.DetectorParameters_create()
    aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_5X5_50)

    time.sleep(2)

    while True:
        ret, frame = video.read()

        # Get Aruco marker
        corners, ids, _ = cv.aruco.detectMarkers(
            frame, aruco_dict, parameters=parameters)

        # Draw polygon around the marker
        int_corners = np.int0(corners)
        #cv.polylines(frame, int_corners, True, (0, 255, 0), 2)

       
        # get id when there are ids
        if len(int_corners) > 0:
            totalAruco = int((len(ids)))
            idList = []
            idGroupList = []
            
            for i in range(totalAruco):            
                #get list with different ids
                idList.append(int(ids[i]))
                
                #get midanIds wich aruco markers are there the most
                idGroupList.append(groupId(int(ids[i])))
               
                print(uniqueIdCornerCheck(idList),idGroupList)

                #collect all corners collering page
                int_id = int((ids[i])%4)
                cornersPage[int_id] = int_corners[i][0][(int((ids[i]+2) % 4))]
                
                #cornes pos
                cv.putText(frame,str(cornersPage[int_id]), cornersPage[int_id],cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 3)
               
                
            #draw the colering page area when all aruco codes are found and there all the same group id 
            if totalAruco == 4 and uniqueIdCornerCheck(idList) == True:
                for j in range(4):
                    cv.line(frame, cornersPage[j], cornersPage[(j+1)%4], (255, 0, 255), 2)
                    
            # what coloring page
            cv.putText(frame,colleringPageName[groupId(ids[0])], (10, 50),
                        cv.FONT_HERSHEY_SIMPLEX, 2, 255, 6)

                
        cv.imshow("cam", frame)
        
        if cv.waitKey(frameRate) == ord('x'):
            
            break

    video.release()
    cv.destroyAllWindows()


main()

# todo transform picture