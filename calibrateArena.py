#!/usr/bin/python

from arena.calibrate import CalibrateObject
import cv2

obj = CalibrateObject()
obj.set_frame(cv2.imread('test.png'))
obj.prepare_image()
obj.read_points()