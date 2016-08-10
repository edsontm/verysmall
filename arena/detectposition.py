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
        frame = cv2.imread('../test.png')
        obj.set_frame(frame)
        obj.find_robots()
        obj.find_ball()


class RobotPosition():
    def __init__(self):
        self.time = robos.LIATime()
        self.frame = None
    def set_frame(self,frame):
        self.frame = frame
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.dframe = cv2.adaptiveThreshold(self.gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 10)


        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

    def _lista_candidatos(self,vcor):
        ret = []
        for robo in self.time.robos:
            for cor in robo.icores:
                cmin = cor[0]
                cmax = cor[1]
                if all(vcor>=cmin) and all(vcor <= cmax):
                    ret.append(robo.id)
        return ret





    def find_robots(self):
        img = self.hsv

        for i in range(len(self.time.robos)):
            robo = self.time.robos[i]
            lres = []
            for j in range(len(robo.icores)):
                cor = robo.icores[j]
                lower = cor[0]
                upper = cor[1]

                res = cv2.inRange(img,lower,upper)
                #janela = 'res'+robo.nome+str(j)
                #cv2.namedWindow(janela)
                #cv2.imshow(janela, res)
                lres.append(res)
            if len(lres) > 1:
                res = cv2.bitwise_or(lres[0],lres[1])
            else:
                res = lres[0]
            janela = 'res' + robo.nome
            cv2.namedWindow(janela)
            cv2.imshow(janela, res)




        key = cv2.waitKey(0) & 0xFF


    def find_ball(self):
        pass

if __name__ == '__main__':
    unittest.main()