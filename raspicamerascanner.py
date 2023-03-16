from picamera.array import PiRGBArray 
from picamera import PiCamera 
import cv2
import cv2.aruco as aruco
import numpy
import time
import RPi.GPIO as GPIO
import board
import neopixel
import argparse
from pythonosc import udp_client


#Gpio pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#ledsetup
PIXEL_PIN = board.D10
NUM_PIXELS_LEDRING = 60
NUM_PIXELS_BOX = 270
NUM_PIXELS = NUM_PIXELS_LEDRING + NUM_PIXELS_BOX
ORDER = neopixel.GRB

#camera setup
#CAMERAWIDTH = int(1440)
#CAMERAHEIGHT = int(810)
#FRAME_RATE = 40

#camera setup
CAMERAWIDTH = int(1080)
CAMERAHEIGHT = int(607)
FRAME_RATE = 40

#colering pages lis
COLLERING_PAGE_NAME = ['Gebouw','Raam',]

#output image #landscape mode A4
IMG_OUTPUT_WIDTH = 297*7
IMG_OUTPUT_HEIGHT = 210*7

SHARED_FOlDER = "/home/pi/share"

#setup osc connection
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="192.168.0.20",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)


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
    camera.brightness = 50
    camera.contrast = 50
    camera.exposure_mode = 'night'
    camera.awb_mode = 'shade'
 
    # Generates a 3D RGB array and stores it in rawCapture
    raw_capture = PiRGBArray(camera, size=(CAMERAWIDTH, CAMERAHEIGHT))
 
    # Wait a certain number of seconds to allow the camera time to warmup
    time.sleep(4)
    
    # Load Aruco detectorx
    parameters = cv2.aruco.DetectorParameters_create()
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

    #set corners for collering page
    corners_page = [(0,0),(0,0),(0,0),(0,0)] # [leftTop,rightTop,rightBottom,leftBottom]
    converted_points = numpy.float32(
            [[0, 0], [IMG_OUTPUT_WIDTH, 0], [0, IMG_OUTPUT_HEIGHT], [IMG_OUTPUT_WIDTH, IMG_OUTPUT_HEIGHT]])

    #set pixels
    pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=1, auto_write=False, pixel_order=ORDER)

    #bolean for making a picture
    picture_ready = False

    button_pressed =False

    send_switch = False


    def pixels_scanned_correct():
        for i in range(NUM_PIXELS_LEDRING):
            pixels[i] = (180, 180, 180)
        for j in range(NUM_PIXELS_BOX):
            pixels[NUM_PIXELS_LEDRING+j] = (0, 8, 0)
        pixels.show()

    def pixels_scanned_uncorrect():
        for i in range(NUM_PIXELS_LEDRING):
            pixels[i] = (128, 128, 128)
        for j in range(NUM_PIXELS_BOX):
            pixels[NUM_PIXELS_LEDRING+j] = (0, 0, 8)
        pixels.show()

    #pixelbrightness
    pb = 120

    def pixels_white():
        for i in range(NUM_PIXELS_LEDRING):
            pixels[i] = (0, 0, 0)
        for j in range(NUM_PIXELS_BOX):
            pixels[NUM_PIXELS_LEDRING+j] = (pb, pb, pb)
        pixels.show()

    def pixels_loading():
        for i in range(NUM_PIXELS_LEDRING):
            pixels[i] = (0, 0, 0)
        #for j in range(NUM_PIXELS_BOX):
        #    pixels[NUM_PIXELS_LEDRING+j] = (255,234, 0)
        pixels.show()
        pixels.fill((0, 0, 0))
        for t in range(102):  # 102
            pixels[NUM_PIXELS_LEDRING+t] = (8, 6, 0)
            pixels[NUM_PIXELS_LEDRING+t+85] = (8, 6, 0)

            #pixels[NUM_PIXELS_LEDRING+NUM_PIXELS_BOX-t-85] = (8,6, 0)
            #pixels[NUM_PIXELS_LEDRING+NUM_PIXELS_BOX-t-165-22] = (8,6, 0)

            pixels.show()
            #time.sleep(0.16666)
    


    #draw loop
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

        frame = frame.array
        original_frame = frame.copy()

        # Get Aruco marker
        corners, ids, _ = cv2.aruco.detectMarkers(
            frame, aruco_dict, parameters=parameters)

        # Draw polygon around the marker
        int_corners = numpy.int0(corners)
        #cv2.polylines(frame, int_corners, True, (0, 255, 0), 2)
       
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
                #cv2.putText(frame,str(corners_page[int_id]), corners_page[int_id],cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 3)
            

            if picture_ready:

                    #warps  scanned picture 
                input_points = numpy.float32(
                    [corners_page[0], corners_page[3], corners_page[1], corners_page[2]])
                matrix = cv2.getPerspectiveTransform(
                    input_points, converted_points)
                img_output = cv2.warpPerspective(
                    original_frame, matrix, (IMG_OUTPUT_WIDTH, IMG_OUTPUT_HEIGHT))
                    img_output = cv2.rotate(
                        img_output, cv2.cv2.ROTATE_90_CLOCKWISE)

                    # make a picture from the lighted image
                    cv2.imshow("Warped perspective", img_output)
                    cv2.imwrite('/home/pi/share/scan.jpg', img_output)


                    send_switch = not send_switch

                    #f = open('/home/pi/share/data.txt', 'w')
                    #f.write(str(int(send_switch)))
                    #f.close()

                    #length of animation
                    #new animation
                    #pixels_loading()
                    picture_ready = False
                    button_pressed = False
                        

                        


                    
    

            #only draw the colering page area when all aruco codes are found and there all the same group id 
            if total_aruco == 4 and uniqueIdCornerCheck(id_list) == True and picture_ready == False:
               
                pixels_scanned_correct()

                #draw lines around the scanned picture
                for j in range(2):
                    cv2.line(frame, corners_page[j], corners_page[(
                        j+1) % 4], (255, 0, 255), 2)
                
                button_value = GPIO.input(17) 
                if (button_value == True or button_pressed == True):
                    pixels_white()
                    client.send_message("/button", 1)
                    time.sleep(0.5)


                    picture_ready = True
                    client.send_message("/button", 0)
                    #button_pressed = False
                    

            #when no 4 aruco codes are found   
            else:
                pixels_scanned_uncorrect()

            # shows name scanned colering page
            #cv2.putText(frame,COLLERING_PAGE_NAME[groupId(ids[0])], (10, 50),
             #           cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 6)

        else:
            pixels_scanned_uncorrect()

        cv2.imshow("cam", frame)
        
        # Clear the stream in preparation for the next frame
        raw_capture.truncate(0)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            break
        if key == ord("p"):
            button_pressed = True
            
    #cv2.destroyAllWindows()
    pixels.fill((0, 0, 0))
    pixels.show()

main()

