import unittest
import numpy as np
import json
import os
import copy

class test(unittest.TestCase):
    def test_parameters(self):
        obj = LIAParameters()
        for num in range(0,10):
            min = [0,0,0]
            max = [255,255,255]
            cores = (min,max)
            obj.robo_cor(num,cores)
        x1 = 0
        y1 = 0
        x2 = 40
        y2 = 40
        limites = (x1,y1,x2,y2)
        obj.limites_crop(limites)
        print json.dumps(obj.limites)
        print json.dumps(obj.robo_cores)
        obj.save()
    def test_load(self):
        obj = LIAParameters()
        obj.load()

def jdefault(o):
    return o.__dict__

class LIAParameters:
    def __init__(self):
        self.file_name = 'params.json'
        self.robo_cores = [None]*10
        self.limites = None
        self.thsv_limites = None
        if os.path.isfile(self.file_name):
            self.load()


    def robo_cor(self,num,cores=None):
        if cores != None:
            self.robo_cores[num] = copy.copy(cores)
        return self.robo_cores[num]

    def limites_crop(self,limites = None):
        if limites != None:
            self.limites = limites
        return self.limites

    def limites_thsv(self,limites):
        if limites != None:
            self.thsv_limites = limites
        return self.thsv_limites


    def save(self):
        f = open(self.file_name, 'w')
        json.dump(self.__dict__,f)
        f.close()

#    json.dump(self, f, default=jdefault)

    def load(self):
        with open(self.file_name, 'r') as f:
            data = json.load(f)
            self.file_name    = data['file_name']
            self.robo_cores   = data['robo_cores']
            self.limites      = data['limites']
            self.thsv_limites = data['thsv_limites']




if __name__ == '__main__':
    unittest.main()