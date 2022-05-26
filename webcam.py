import cv2 as cv
from matplotlib import pyplot as plt

cap = cv.VideoCapture(0)
ret, frame = cap.read()