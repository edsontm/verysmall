#!/usr/bin/python
import cv2
import sys
from arena.config import LIAParameters
from arena.cropper import Cropper

if __name__ == '__main__':
    obj = LIAParameters()

    if len(sys.argv) !=2:
        print "usage: %s <image_file>"%(sys.argv[0])
        sys.exit(0)

    frame = cv2.imread(sys.argv[1])
    cropper = Cropper(frame)

    cv2.namedWindow('setBoundaries')
    cv2.setMouseCallback('setBoundaries', cropper.mouse_set_boundaries)
    cv2.imshow('setBoundaries', frame)
    print "Pressione S para salvar"
    key = cv2.waitKey(0) & 0xFF
    if key == ord('s'):
        if cropper.cropped:
            obj.limites_crop(cropper.crop_coordinates)
            obj.save()
            print 'Crop salvo'

