import unittest
import numpy as np
import json


class test(unittest.TestCase):
    def test_parameters(self):
        obj = Parameters()
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
        obj = Parameters()
        obj.load()

def jdefault(o):
    return o.__dict__

class Parameters:
    def __init__(self):
        self.file_name = 'params.json'
        self.robo_cores = [None]*10
        self.limites = None

    def robo_cor(self,num,cores=None):
        if cores != None:
            self.robo_cores[num] = cores

        return self.robo_cores[num]
    def limites_crop(self,limites = None):
        if limites != None:
            self.limites = limites
        return limites
    def save(self):
        with open(self.file_name, 'w') as f:
            json.dump(self, f,default=jdefault)

    def load(self):
        with open(self.file_name, 'r') as f:
            data = json.load(f)
            self.file_name = data['file_name']
            self.robo_cores = data['robo_cores']
            self.limites = data['limites']
            print "limites",self.limites[0]+1



if __name__ == '__main__':
    unittest.main()