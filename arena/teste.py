#!/usr/bin/python
import numpy as np

import cv2

import unittest
from sklearn.cluster import KMeans
import scipy
import robos


class CalibrateTest(unittest.TestCase):
    def test_find(self):
        obj = CalibrateObject()
        obj.set_frame(cv2.imread('/home/edsont/imagem.tif'))
        obj.prepare_image()
        obj.read_points()



class CalibrateObject():
    def __init__(self):
        self.centers = None
        self.frame = None
        self.hsv = None
        self.frame_undo = None
        self.mouse_click = None
        self.square_train = 30
        self.hsv = None
        self.clicked = False
        self.nrobo = 0
        self.time = robos.LIATime()
        self.enable_mean_shift = True
        self.actual_hcolor = []


    def set_frame(self, frame):
        self.frame = frame
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
      #  self.hsv = cv2.erode(self.hsv, None, iterations=2)
      #  self.hsv = cv2.dilate(self.hsv, None, iterations=2)


    def _marca(self,x,y):
        print x, y
        print self.frame[y][x]
        print self.hsv[y][x]

        n_clusters = 2
        (x, y) = self.mouse_click

        colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (128, 128, 128)]
        instances = []
        xmin = x - self.square_train
        xmax = x + self.square_train
        ymin = y - self.square_train
        ymax = y + self.square_train

        img = np.zeros((ymax - ymin, xmax - xmin,3), np.uint8)
        img.fill(255)

        for j in range(xmin, xmax):
            for i in range(ymin, ymax):
                instances.append(self.hsv[i][j])
        kmeans = KMeans(n_clusters=n_clusters)
        result = kmeans.fit_predict(instances)



        k = 0
        print result
        counts = np.bincount(result)
        maj = 1
        if counts[0] > counts[1]:
            maj = 0



        print counts
        #print unique

        for j in range(0, xmax - xmin):
            for i in range(0, ymax - ymin):
                if result[k] == maj:
                    img[i][j] = [0,0,0]
                else:
                    img[i][j] = [255,255,255]
                k += 1


     #   ret,markers = cv2.connectedComponent




        img = cv2.pyrMeanShiftFiltering(img, 21, 51)
        img = cv2.erode(img, None, iterations=2)
        img = cv2.dilate(img, None, iterations=2)


        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel, iterations = 2)
        sure_bg = cv2.dilate(opening,kernel,iterations=2)

        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,0.2*dist_transform.max(),255,0)


        sure_fg = np.uint8(sure_fg)

        components = cv2.bitwise_and(gray,sure_fg)


        im2, contours, hierarchy = cv2.findContours(components, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        print "contour %d"%(len(contours))
        hsv = self.hsv
        self.time.robos[self.nrobo].cores = []
        print "robo",self.nrobo
        self.actual_hcolor = []
        for cnt in contours:
            (x,y) = cnt[0][0]

            if img[y][x][0] > 250:
                print 'new contour'
                cv2.drawContours(img, [cnt], 0, (0,255,0), 3)
                hcolor=[]
                for ccord in cnt:
                    (x,y) = ccord[0]
                    x += xmin
                    y += ymin

                    if hsv[y][x][0] > 0:
                        print hsv[y][x][0]
                        hcolor.append(hsv[y][x][0])
                self.actual_hcolor.append(hcolor)

        img2 = np.copy(img)
        cv2.drawContours(img2, contours, -1, (255, 0, 0), 3)


     #   markers = cv2.watershed(img,markers)
     #   img[markers == -1] = [0,0,255]
        cv2.namedWindow('res')
        cv2.imshow('res',img)


    def mouse_callback(self, event, x, y, flags, param):
#        if event == cv2.EVENT_MOUSEMOVE:

        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_click = (x, y)
            self._marca(x,y)
            self.clicked = True



    def prepare_image(self):
        cv2.namedWindow('readpos')
        cv2.setMouseCallback('readpos', self.mouse_callback)
        cv2.imshow('readpos', self.frame)


    def read_points(self):

        sair = False

        while(not sair):
            print self.time.lista_robos()
            print "Digite o numero do robo ou q para sair:"
            key = cv2.waitKey(0) & 0xFF
            if key >= ord('0') and key <= ord('9'):
                nrobo = int(key) - ord('0')
                if nrobo < self.time.nrobos:
                    self.nrobo = nrobo
                    print "===== craque da camisa %d - %s escolhido =====" %(self.nrobo,self.time.robos[self.nrobo].nome)
            if key == ord('s'):
                self.time.robos[self.nrobo].lcores = self.actual_hcolor
                self.time.robos[self.nrobo].atualiza_icores()
                self.time._salva_init()

                hsv = np.copy(self.hsv)

                cmin = self.time.robos[self.nrobo].icores[0][0]
                cmax = self.time.robos[self.nrobo].icores[0][1]
                lower = np.array([cmin, 50, 50])
                upper = np.array([cmax, 255, 255])
                resultado1 = cv2.inRange(hsv, lower, upper)
                cv2.namedWindow('resultado1')
                cv2.imshow('resultado1', resultado1)

                if len(self.time.robos[self.nrobo].icores) == 2:

                    cmin = self.time.robos[self.nrobo].icores[1][0]
                    cmax = self.time.robos[self.nrobo].icores[1][1]
                    lower = np.array([cmin, 50, 50])
                    upper = np.array([cmax, 255, 255])
                    resultado2 = cv2.inRange(hsv, lower, upper)

                    resultado = cv2.bitwise_or(resultado1, resultado2)
                    cv2.namedWindow('resultado2')
                    cv2.imshow('resultado2', resultado2)
                    cv2.namedWindow('resultados')
                    cv2.imshow('resultados', resultado)

                print "salvo"


            if key == ord('q'):
                sair = True



class CalibrateObjectCluster():
    def __init__(self):
        self.centers = None
        self.frame = None
        self.mouse_click = None
        self.square_train = 20
        self.n_clusters = 3
        self.hsv = None
        self.clicked = False

    def set_frame(self,frame):
        self.frame = frame

    def mouse_callback(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_click = (x,y)
            print x,y
            print self.frame[y][x]
            self.clicked = True

        
    def read_position(self): 
        cv2.namedWindow('readpos')
        cv2.setMouseCallback('readpos',self.mouse_callback)
        cv2.imshow('readpos',self.frame)


    def find_clusters(self):
        (x,y) = self.mouse_click
        point = self.frame[y][x]
        instances = []
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        for j in range(x-self.square_train,x+self.square_train):
            for i in range(y-self.square_train,y+self.square_train):
                instances.append(self.hsv[i][j])
        self.kmeans = KMeans(n_clusters=self.n_clusters)
        self.kmeans.fit(instances)
    def show_clusters(self):
        (x,y) = self.mouse_click
        img = np.zeros(self.hsv.shape,np.uint8)
        img.fill(255)
        colors = [(0,0,255),(255,0,0),(0,255,0),(128,128,128)]
        instances = []
        centers = self.kmeans.cluster_centers_
        for j in range(x-self.square_train,x+self.square_train):
            for i in range(y-self.square_train,y+self.square_train):
                instance = self.hsv[i][j]
                dist = float('inf')
                selected_color = 0
                for k in range(len(centers)):
                    center = centers[k]
                    d = scipy.spatial.distance.euclidean(center, instance)
                    print d,k
                    if d < dist:
                        dist = d
                        selected_color = k
                self.frame[i][j] = colors[selected_color]
                print 'selected',selected_color
                k+=1
        cv2.imshow('result',self.frame)
        cv2.waitKey(0)


        
           

if __name__ == '__main__':
    unittest.main()
        
    
    
