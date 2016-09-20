import cv2
import numpy as np
from sklearn.neighbors import NearestNeighbors


class Mascara(object):
    def __init__(self,frame = None):
        self.start = None
        self.end = None
        self.frame = frame
        self.mask_dimentions = 200
        self.grid_size = 10
        self.mask = None
        self.nbrs = None
        self.build_mask()
        
        
    def build_mask(self):
        tx = []
        for i in range(0,self.mask_dimentions,self.grid_size):
            for j in range(0,self.mask_dimentions,self.grid_size):
                tx.append([i,j])
        X = np.array(tx)
        self.nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(X)





    def mouse_create_vector(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            neigbor = self.nbrs.kneighbors([x,y])
            print neigbor
            self.start = (x,y)
            self.frame_undo = self.frame.copy()
            self.clicked = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.clicked:
                print (x, y)
                if len(self.boundaries) == 1:
                    tframe = self.frame_undo.copy()
                    cv2.line(tframe,self.start,(x,y),(0,0,255),2)
                    self.frame = tframe
                    cv2.imshow('setBoundaries',tframe)
        elif event == cv2.EVENT_LBUTTONUP:
            if self.clicked:
                self.clicked = False
                self.end = (x, y)

        
        
if __name__ == '__main__':
    obj = Mascara()
    max_size = obj.mask_dimentions
    img = np.zeros((max_size,max_size,3), np.uint8)
    img.fill(255)
    obj.frame = img
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',obj.mouse_create_vector)
    while(1):
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()

    
