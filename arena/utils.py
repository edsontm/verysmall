import unittest

import cv2
import numpy as np
import copy

from config import LIAParameters
from cropper import Cropper

class Region():
    def __init__(self):
        self.max = [-1,-1,-1]
        self.min = [256,256,256]
    def set(self,m):
        # min
        for i in range(3):
            if m[i] < self.min[i]:
                self.min[i] = m[i]
        # max
        for i in range(3):
            if m[i] > self.max[i]:
                self.max[i] = m[i]

class SeekRobots():
    def __init__(self):
        self.frame = None
        self.crop = Cropper()
        self.p = LIAParameters()
        self.crop.crop_coordinates = self.p.limites


    def set_frame(self, frame):
        self.frame = self.crop.crop(frame)
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        tmin = np.array(self.p.thsv_limites[0])
        tmax = np.array(self.p.thsv_limites[1])
        self.thsv = cv2.inRange(self.hsv, tmin, tmax)
        self.hsv = cv2.bitwise_and(self.hsv, self.hsv, mask=self.thsv)
        self.frame = cv2.bitwise_and(self.frame, self.frame, mask=self.thsv)

    def ball(self):
        tmin = np.array(self.p.robo_cores[0][0])
        tmax = np.array(self.p.robo_cores[0][1])
        thsv = cv2.inRange(self.hsv, tmin, tmax)
        im2,contours, hierarchy = cv2.findContours(thsv,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            lcnt = float(len(cnt))
            lx = 0
            ly = 0
            if lcnt > 2:
                for tpoint in cnt:
                    (tx, ty) = tpoint[0]
                    lx += tx
                    ly += ty
                tx = (int(lx/lcnt))
                ty = (int(ly/lcnt))
                cv2.circle(self.frame,(tx,ty),5,(0,255,0),thickness=-1)
                cv2.putText(self.frame, 'bola', (tx,ty), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))


        

    def home_team(self):
        # cor time 1
        self.p.robo_cores[1][0]
        boundary = 20

        tmin = np.array(self.p.robo_cores[1][0])
        tmax = np.array(self.p.robo_cores[1][1])
        thsv = cv2.inRange(self.hsv, tmin, tmax)


        im2,contours, hierarchy = cv2.findContours(thsv,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        rcenters = []
        # pega cor do time
        for cnt in contours:
            lcnt = float(len(cnt))
            lx = 0
            ly = 0
            if lcnt > 2:
                for tpoint in cnt:
                    (tx, ty) = tpoint[0]
                    lx += tx
                    ly += ty
                tx = (int(lx/lcnt))
                ty = (int(ly/lcnt))
                cv2.circle(self.frame,(tx,ty),5,(0,255,0),thickness=-1)
                rcenters.append((tx,ty))
        # cria o patch 
        for rcenter in rcenters:
            x1 = rcenter[0] - boundary
            y1 = rcenter[1] - boundary
            x2 = rcenter[0] + boundary
            y2 = rcenter[1] + boundary
            patch = self.hsv[y1:y2, x1:x2]
            patchrgb = self.frame[y1:y2, x1:x2]




            achou = False
            crobot = [0]*5
            crobot_pos = [None]*5
            # 2 vermelhor
            # 3 roxo
            # 4 verde

            # escolhendo o robo da imagem

            for nrobo in range(2,5):
                #print "ROBO   ", nrobo
                tmin = np.array(self.p.robo_cores[nrobo][0])
                tmax = np.array(self.p.robo_cores[nrobo][1])
                robo = cv2.inRange(patch, tmin, tmax)
                mask = cv2.inRange(self.hsv, tmin, tmax)
                cv2.imshow('saida1', mask)
                cv2.imshow('saida2',robo)
                cv2.imshow('patch',patchrgb)
                #cv2.waitKey(0)
                im2,contours, hierarchy = cv2.findContours(robo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)




                maxcnt = 0
                selectedcnt = None
                for cnt in contours:
                    lcnt = len(cnt)
                    if lcnt >maxcnt:
                        maxcnt = lcnt
                        selectedcnt = cnt
                lx = 0
                ly = 0
                #print maxcnt
                if maxcnt >= 1:
                    lcnt = float(maxcnt)
                    #print maxcnt
                    for tpoint in selectedcnt:
                        (tx, ty) = tpoint[0]
                        #if tx > x1 and tx < x2:
                        #    if ty > y1 and ty < y2:
                        lx += tx 
                        ly += ty
                    crobot[nrobo] += maxcnt
                    tx = (int(lx / lcnt)) + x1
                    ty = (int(ly / lcnt)) + y1
                    dist = abs(rcenter[0] - tx) + abs(rcenter[1] - ty)
                    #if dist > 5  and dist < 20:
                    crobot_pos[nrobo] = (tx,ty)
                    achou = True
                    cv2.drawContours(robo, [selectedcnt], 0, (0, 255, 0), 3)
                    cv2.imshow('saida', robo)
            if achou:
                srobot = np.argmax(crobot)
                #print crobot
                #print srobot

                cv2.putText(self.frame, '%d' % (srobot), crobot_pos[srobot], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
                cv2.circle(self.frame, crobot_pos[srobot], 5, (0, 0, 255), thickness=-1)

            # robo2
            # robo3






                #cv2.drawContours(self.frame, [cnt], 0, (0, 255, 0), 3)




class GetColor():
    def __init__(self):
        self.frame = None
        self.crop = Cropper()
        self.p = LIAParameters()
        self.crop.crop_coordinates = self.p.limites
        self.x = None
        self.y = None
        self.region = Region()

    def reset(self):
        self.x = None
        self.y = None
        self.region = Region()


    def set_frame(self,frame):
        self.frame = self.crop.crop(frame)
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        tmin = np.array(self.p.thsv_limites[0])
        tmax = np.array(self.p.thsv_limites[1])
        self.thsv = cv2.inRange(self.hsv,tmin,tmax)
        self.hsv = cv2.bitwise_and(self.hsv,self.hsv,mask=self.thsv)
        self.frame = cv2.bitwise_and(self.frame,self.frame,mask=self.thsv)

    def mouse_callback(self, event, x, y, flags, param):
        self.x = x
        self.y = y
        if event == cv2.EVENT_MOUSEMOVE:
            text_msg = '%d %d'%(x,y)

        elif event == cv2.EVENT_LBUTTONUP:
            box = 1
            x1 = x - box
            x2 = x + box
            y1 = y - box
            y2 = y + box

            cframe = self.hsv[y1:y2,x1:x2]
            for line in cframe:
                for cols in line:
                    if cols[0] !=0:
                        self.region.set(cols.tolist())
            tmin = np.array(self.region.min)
            tmax = np.array(self.region.max)
            thsv = cv2.inRange(self.hsv, tmin, tmax)
            cv2.rectangle(self.frame,(x1,y1),(x2,y2),(0,0,255),1)

            cv2.namedWindow('patch')
            cv2.imshow('patch',thsv)
            cv2.imshow('frame',self.frame)





    def get_color(self):
        cv2.namedWindow('frame')

        cv2.setMouseCallback('frame',self.mouse_callback)
        cv2.imshow('frame',self.frame)




