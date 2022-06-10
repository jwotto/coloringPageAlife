from pickle import FALSE, TRUE
import cv2 as cv
from pandas import array
import cv2.aruco as aruco
import numpy as np
import time

#camera setup
CAMERA = 1
CAMERAWIDTH = 1280
CAMERAHEIGHT = 720
FRAMERATE = 30

#colering pages lis
COLLERING_PAGE_NAME = ['Gebouw','Raam',]

FRAMERATE = int(1000/FRAMERATE)

#output image #landscape mode
IMG_OUTPUT_WIDTH = 297*4
IMG_OUTPUT_HEIGHT = 210*4

#returns the group id dor example id 0 to 3 is group 0 and id 4 to 7 is group 1
def groupId(id):
    id = (id - (id%4)) /4
    return int(id)

#are there 4 unique codes with the same group id?
def uniqueIdCornerCheck(idList):
    id_sum = 0 
    if len(idList) == 4:
        for i in range(4):   
            id_sum += ((idList[i]%4)+1)
        if id_sum == 10: # because 1+2+3+4 = 10
            return True
        else: 
            return False
    else:
        return False


def main():
    # set video capture
    video = cv.VideoCapture(CAMERA)
    video.set(3, CAMERAWIDTH)
    video.set(4, CAMERAHEIGHT)

    # Load Aruco detectorx
    parameters = cv.aruco.DetectorParameters_create()
    aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_5X5_50)

    #wait time dor camera to startup
    time.sleep(2)
    
    #set corners for collering page
    corners_page = [(0,0),(0,0),(0,0),(0,0)] # [leftTop,rightTop,rightBottom,leftBottom]
    converted_points = np.float32(
            [[0, 0], [IMG_OUTPUT_WIDTH, 0], [0, IMG_OUTPUT_HEIGHT], [IMG_OUTPUT_WIDTH, IMG_OUTPUT_HEIGHT]])

    while True:
        ret, frame = video.read()
        original_frame = frame.copy()

        # Get Aruco marker
        corners, ids, _ = cv.aruco.detectMarkers(
            frame, aruco_dict, parameters=parameters)

        # Draw polygon around the marker
        int_corners = np.int0(corners)
        cv.polylines(frame, int_corners, True, (0, 255, 0), 2)

       
        # get id when there are ids
        if len(int_corners) > 0:
            total_aruco = int((len(ids)))
            id_list = []
            id_group_list = []
            
            for i in range(total_aruco):            
                #get list with different ids
                id_list.append(int(ids[i]))
                
                #get midanIds wich aruco markers are there the most
                id_group_list.append(groupId(int(ids[i])))

                #collect all corners collering page
                int_id = int((ids[i])%4)
                corners_page[int_id] = int_corners[i][0][(int((ids[i]+2) % 4))]
                
                #shows cornes positions on screen
                cv.putText(frame,str(corners_page[int_id]), corners_page[int_id],cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 3)
               
                
            #only draw the colering page area when all aruco codes are found and there all the same group id 
            if total_aruco == 4 and uniqueIdCornerCheck(id_list) == True:
                
                #draw lines around the scanned picture
                for j in range(4):
                    cv.line(frame, corners_page[j], corners_page[(j+1)%4], (255, 0, 255), 2)
                
                #warps  scanned picture 
                input_points = np.float32([corners_page[0],corners_page[3],corners_page[1],corners_page[2]])
                matrix = cv.getPerspectiveTransform(input_points, converted_points)
                img_output = cv.warpPerspective(
                original_frame, matrix, (IMG_OUTPUT_WIDTH, IMG_OUTPUT_HEIGHT))
                img_output = cv.rotate(img_output, cv.cv2.ROTATE_90_CLOCKWISE)
                cv.imshow("Warped perspective", img_output)
                 
            # shows name scanned colering page
            cv.putText(frame,COLLERING_PAGE_NAME[groupId(ids[0])], (10, 50),
                        cv.FONT_HERSHEY_SIMPLEX, 2, 255, 6)

                
        cv.imshow("cam", frame)
        
        if cv.waitKey(FRAMERATE) == ord('x'):
            
            break

    video.release()
    cv.destroyAllWindows()


main()

