#!/usr/bin/python
import cv2
import numpy as np




cv2.namedWindow('main')

cap = cv2.VideoCapture('output.avi')


while(cap.isOpened()):
    ret,frame = cap.read()
    cv2.imshow('main',frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord ('s'):
        cv2.imwrite('test.png',frame)
        cv2.namedWindow('captured')
        cv2.imshow('captured',frame)
        cv2.waitKey(0)



