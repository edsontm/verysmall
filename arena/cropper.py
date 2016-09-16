import cv2
from config import LIAParameters


class Cropper:
    def __init__(self,frame=None,crop_coordinates=None,parameters = None):
        self.frame = frame
        self.crop_coordinates = crop_coordinates
        self.frame_cropped = None
        self.boundaries = []
        self.clicked = False
        self.cropped = False
        if isinstance(parameters,LIAParameters):
            print parameters.limites
            self.crop_coordinates = parameters.limites

    def mouse_set_boundaries(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.boundaries.append((x,y))
            self.frame_undo = self.frame.copy()
            self.clicked = True
        elif event == cv2.EVENT_MOUSEMOVE:

            if self.clicked:
                print (x, y)
                if len(self.boundaries) == 1:
                    tframe = self.frame_undo.copy()
                    cv2.rectangle(tframe,self.boundaries[-1],(x,y),(0,0,255),2)
                    self.frame = tframe
                    cv2.imshow('setBoundaries',tframe)
        elif event == cv2.EVENT_LBUTTONUP:
            if self.clicked:
                self.clicked = False
                self.boundaries.append((x, y))
                self.crop_frame_show()



    def crop_frame_show(self):
        if len(self.boundaries) == 2:
            (x1,y1) = self.boundaries[0]
            (x2,y2) = self.boundaries[1]
            roi = self.frame[y1:y2,x1:x2]
            self.frame = roi
            cv2.imshow('readpos',self.frame)
            self.crop_coordinates = [x1,y1,x2,y2]
            self.cropped = True


    def crop(self,frame):
        (x1, y1,x2, y2) = self.crop_coordinates
        self.frame_cropped = frame[y1:y2, x1:x2]
        return self.frame_cropped




