#!/usr/bin/python

import numpy as np

import cv2

import unittest
from sklearn.cluster import KMeans
import scipy
import robos

class teste(unittest.TestCase):
    def teste1(self):
        obj = RobotPosition()
        print(obj.time.lista_robos())
        obj.find_robots()
        obj.find_ball()


class RobotPosition():
    def __init__(self):
        self.time = robos.LIATime()

    def find_robots(self):
        pass
    def find_ball(self):
        pass

if __name__ == '__main__':
    unittest.main()