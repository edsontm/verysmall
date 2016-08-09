import csv
import numpy as np


class LIATime():
    def __init__(self,nrobos = 3):
        self.nrobos = nrobos
        self.robos = []
        self._load_init()
    def _load_init(self):
        f = csv.DictReader(open('init.csv'),delimiter =',')
        for row in f:
            self.robos.append(LIARobo(row['id'],row['nome']))
    def lista_robos(self):
        tstr = ''
        for robo in self.robos:
            tstr += '%s %s\n'%(robo.id,robo.nome)
        return tstr
    def _save_init(self):
        f = open('init.csv','w')
        f.write('id,nome,cor1,cor2\n')
        for robo in self.robos:
            f.write(robo.salva_str()+'\n')



class LIARobo():
    def __init__(self,id,nome):
        self.id = id
        self.nome = nome
        self.lcores = []
        self.icores = []
        self.ccores = []

    def atualiza_icores(self):
        self.icores = []
        if len(self.lcores) == 2:
            for lcor in self.lcores:
                max = np.max(lcor)
                min = np.min(lcor)
                self.icores.append((min,max))
    def salva_str(self):
        tstr = '%s,%s'%(self.id,self.nome)
        if len(self.icores) == 2:
            tstr += '(%d:%d),(%d,%d)'%(self.icores[0][0],self.icores[0][1], self.icores[1][0],self.icores[1][1])
        return tstr
