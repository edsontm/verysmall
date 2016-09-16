#!/usr/bin/python

from arena.utils import SeekRobots
import cv2



a = SeekRobots()


cv2.namedWindow('main')

cap = cv2.VideoCapture('output.avi')



while(cap.isOpened()):
    ret,frame = cap.read()
    a.set_frame(frame)
    a.home_team()
    cv2.imshow('main',a.frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break