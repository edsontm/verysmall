#!/usr/bin/python

from arena.utils import GetColor
from arena.config import LIAParameters
import cv2
import numpy as np


def _print_msg(vet):
    for i in range(len(vet)):
        print '%d - %s'%( i,vet[i])
    print 'q - quit'
    print 's - save'
    print 'space - ignore previous colors'

p = LIAParameters()
obj = GetColor()
key = 10
msg = ['bola','ararabot_cor','robo1','robo2','robo3', 'adversario_cor','arobo1','arobo2','arobo3']
sair = False
_print_msg(msg)

cap = cv2.VideoCapture(1)

while(not sair):
    ret,frame = cap.read()
    #frame = cv2.imread('test.png')
    obj.set_frame(frame)

    obj.get_color()
    key = cv2.waitKey(1) & 0xFF
    print key
    if key >= ord('0') and key <=ord('8'):
        index = key - ord('0')
        print key,index,msg[index]
        print [obj.region.min,obj.region.max]
        p.robo_cor(index,[obj.region.min,obj.region.max])
        print p.robo_cores

    elif key == ord('q'):
        sair = True
    elif key == ord('s'):
        p.save()
        print 'saved'
    elif key == ord(' '):
        obj.reset()



