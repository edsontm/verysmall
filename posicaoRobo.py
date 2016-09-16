#!/usr/bin/python

from arena.utils import SeekRobots
import cv2



a = SeekRobots()


cv2.namedWindow('main')

cap = cv2.VideoCapture(1)



while(cap.isOpened()):
    ret,frame = cap.read()
    a.set_frame(frame)
    a.ball()
    a.home_team()
    cv2.imshow('main',a.frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
