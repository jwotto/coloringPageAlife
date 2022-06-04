import cv2 as cv
import cv2.aruco as aruco
import numpy as np
import time


camera = 0
cameraWidth = 1280
cameraHeight = 720
frameRate = 60


frameRate = int(1000/frameRate)


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
        cv.polylines(frame, int_corners, True, (0, 255, 0), 2)

        # get id when there are ids
        if len(int_corners) > 0:

            totalAruco = int((len(ids)))

            for i in range(totalAruco):
                cv.putText(frame, str(ids[i]), int_corners[i][0][2],
                           cv.FONT_HERSHEY_SIMPLEX, 1, 255, 3)

            # what coloring page
            if ids[0] <= 3:
                cv.putText(frame, "Gebouw", (10, 50),
                           cv.FONT_HERSHEY_SIMPLEX, 2, 255, 6)
            if ids[0] >= 4 and ids[[0]] < 7:
                cv.putText(frame, "Raam", (10, 50),
                           cv.FONT_HERSHEY_SIMPLEX, 2, 255, 6)

        cv.imshow("cam", frame)
        if cv.waitKey(frameRate) == ord('x'):
            break

    video.release()
    cv.destroyAllWindows()


main()
