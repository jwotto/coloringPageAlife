import numpy as np
import cv2

<<<<<<< HEAD
<<<<<<< HEAD
img = cv2.imread('Photos/Tower_Test.png')
=======
img = cv2.imread('ptrain/tower.png', 0)

>>>>>>> Test_Kleurplaat
=======
img = cv2.imread('ptrain/tower.png', 0)

>>>>>>> Test_Kleurplaat
orb = cv2.ORB_create(100)


kp, des = orb.detectAndCompute(img, None)


# draw only keypoints location,not size and orientation
#img2 = cv2.drawKeypoints(img, kp, None, flags=None)
# Now, let us draw with rich key points, reflecting descriptors. 
# Descriptors here show both the scale and the orientation of the keypoint.
img2 = cv2.drawKeypoints(img, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("With keypoints", img2)
cv2.waitKey(0)

print(kp )