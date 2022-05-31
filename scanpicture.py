
from pickle import TRUE
import cv2 as cv
import numpy as np

last_img_output = None

last_biggest = []

def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv.contourArea(i)
        if area > 90000:
            peri = cv.arcLength(i, True)
            approx = cv.approxPolyDP(i, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
                print(area)
    return biggest


#get webcam camera change numbers for different camera's
video = cv.VideoCapture(0)

while True:
    ret, frame = video.read()
    img_original = frame.copy()

    # Image modification
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.bilateralFilter(gray, 20, 30, 30)
    edged = cv.Canny(gray, 10, 20)

    # Contour detection
    contours, hierarchy = cv.findContours(
        edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)[:10]

    biggest = biggest_contour(contours)

   # when box is detected
    if biggest != []:
        cv.drawContours(frame, [biggest], -1, (255, 0, 0), 7)

        # Pixel values in the original image
        points = biggest.reshape(4, 2)
        input_points = np.zeros((4, 2), dtype="float32")

        points_sum = points.sum(axis=1)
        input_points[0] = points[np.argmin(points_sum)]
        input_points[3] = points[np.argmax(points_sum)]

        points_diff = np.diff(points, axis=1)
        input_points[1] = points[np.argmin(points_diff)]
        input_points[2] = points[np.argmax(points_diff)]

        (top_left, top_right, bottom_right, bottom_left) = input_points
        bottom_width = np.sqrt(
            ((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
        top_width = np.sqrt(
            ((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
        right_height = np.sqrt(
            ((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
        left_height = np.sqrt(
            ((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))

        # Output image size
        max_width = max(int(bottom_width), int(top_width))
        # max_height = max(int(right_height), int(left_height))
        max_height = int(max_width * 1.414)  # for A4

        # Desired points values in the output image
        converted_points = np.float32(
            [[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])

        # Perspective transformation
        matrix = cv.getPerspectiveTransform(input_points, converted_points)
        img_output = cv.warpPerspective(
            img_original, matrix, (max_width, max_height))

        # Image shape modification for hstack
        gray = np.stack((gray,) * 3, axis=-1)
        edged = np.stack((edged,) * 3, axis=-1)

        #prev image
        last_img_output = img_output

        #keep picture one size
        resize_img = cv.resize(last_img_output, (1018, 720))
        rotate_img = cv.rotate(resize_img, cv.cv2.ROTATE_90_CLOCKWISE)

        cv.imshow("Warped perspective", rotate_img)

        
    cv.imshow("cam", frame)
    
    if cv.waitKey(30) == ord('x'): 
        cv.imwrite('output/scan.jpg', rotate_img)
        break
    

video.release()
cv.destroyAllWindows()