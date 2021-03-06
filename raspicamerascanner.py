from picamera.array import PiRGBArray 
from picamera import PiCamera 
import cv2 as cv
import cv2.aruco as aruco
import numpy as np
import time
import RPi.GPIO as GPIO
import board
import neopixel


#Gpio pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#ledsetup
PIXEL_PIN = board.D10
NUM_PIXELS_LEDRING = 60
NUM_PIXELS_BOX = 135
NUM_PIXELS = NUM_PIXELS_LEDRING + NUM_PIXELS_BOX
ORDER = neopixel.GRB

#camera setup
CAMERAWIDTH = int(1280)
CAMERAHEIGHT = int(720)
FRAME_RATE = 40

#colering pages lis
COLLERING_PAGE_NAME = ['Gebouw','Raam',]

#output image #landscape mode A4
IMG_OUTPUT_WIDTH = 297*4
IMG_OUTPUT_HEIGHT = 210*4

SHARED_FOlDER = "/home/pi/share"


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
    camera = PiCamera()
    camera.resolution = (CAMERAWIDTH, CAMERAHEIGHT)
    camera.framerate = FRAME_RATE
 
    # Generates a 3D RGB array and stores it in rawCapture
    raw_capture = PiRGBArray(camera, size=(CAMERAWIDTH, CAMERAHEIGHT))
 
    # Wait a certain number of seconds to allow the camera time to warmup
    time.sleep(2)
    
    # Load Aruco detectorx
    parameters = cv.aruco.DetectorParameters_create()
    aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_5X5_50)

    #set corners for collering page
    corners_page = [(0,0),(0,0),(0,0),(0,0)] # [leftTop,rightTop,rightBottom,leftBottom]
    converted_points = np.float32(
            [[0, 0], [IMG_OUTPUT_WIDTH, 0], [0, IMG_OUTPUT_HEIGHT], [IMG_OUTPUT_WIDTH, IMG_OUTPUT_HEIGHT]])

    #set pixels
    pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=1, auto_write=False, pixel_order=ORDER)

    #bolean for making a picture
    picture_ready = False

    button_pressed =False

    send_switch = False


    def pixels_scanned_correct():
        for i in range(NUM_PIXELS_LEDRING):
            pixels[i] = (0, 255, 0)
        for j in range(NUM_PIXELS_BOX):
            pixels[NUM_PIXELS_LEDRING+j] = (0 ,255 , 0)
        pixels.show()

    def pixels_scanned_uncorrect():
        for i in range(NUM_PIXELS_LEDRING):
            pixels[i] = (0,0,255)
        for j in range(NUM_PIXELS_BOX):
            pixels[NUM_PIXELS_LEDRING+j] = (0,0,255)
        pixels.show()

    def pixels_white():
        for i in range(NUM_PIXELS_LEDRING):
            pixels[i] = (0, 0, 0)
        for j in range(NUM_PIXELS_BOX):
            pixels[NUM_PIXELS_LEDRING+j] = (255 ,255 , 255)
        pixels.show()


    


    #draw loop
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

        frame = frame.array
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
            

            if picture_ready:

                    #warps  scanned picture 
                    input_points = np.float32([corners_page[0],corners_page[3],corners_page[1],corners_page[2]])
                    matrix = cv.getPerspectiveTransform(input_points, converted_points)
                    img_output = cv.warpPerspective(
                    original_frame, matrix, (IMG_OUTPUT_WIDTH, IMG_OUTPUT_HEIGHT))
                    img_output = cv.rotate(img_output, cv.cv2.ROTATE_90_CLOCKWISE)

                    # make a picture from the lighted image
                    cv.imshow("Warped perspective", img_output)
                    cv.imwrite('/home/pi/share/scan.jpg', img_output)

                    send_switch = not send_switch

                    f = open('/home/pi/share/data.txt', 'w')
                    f.write(str(int(send_switch)))
                    f.close()


                    picture_ready = False
                        

                        


                    
    

            #only draw the colering page area when all aruco codes are found and there all the same group id 
            if total_aruco == 4 and uniqueIdCornerCheck(id_list) == True and picture_ready == False:
               
                pixels_scanned_correct()

                #draw lines around the scanned picture
                for j in range(2):
                    cv.line(frame, corners_page[j], corners_page[(j+1)%4], (255, 0, 255), 2)
                
                button_value = GPIO.input(17) 
                if (button_value == True or button_pressed == True):
                    pixels_white()
                    time.sleep(1)
                    picture_ready = True
                    button_pressed = False
                    

            #when no 4 aruco codes are found   
            else:
                pixels_scanned_uncorrect()

            # shows name scanned colering page
            cv.putText(frame,COLLERING_PAGE_NAME[groupId(ids[0])], (10, 50),
                        cv.FONT_HERSHEY_SIMPLEX, 2, 255, 6)

        else:
            pixels_scanned_uncorrect()

        cv.imshow("cam", frame)
        
        # Clear the stream in preparation for the next frame
        raw_capture.truncate(0)

        key = cv.waitKey(1) & 0xFF
        if key == ord("x"):
            break
        if key == ord("p"):
            button_pressed = True
            

    #cv.destroyAllWindows()
    pixels.fill((0, 0, 0))
    pixels.show()

main()

