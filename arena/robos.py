import csv
import numpy as np


class LIATime():
    def __init__(self,nrobos = 3):
        self.nrobos = nrobos
        self.robos = []
        self._carrega_init()
    def _carrega_init(self):
        f = csv.DictReader(open('init.csv'),delimiter =',')
        for row in f:
            obj = LIARobo(row['id'],row['nome'])
            if row['cor1'] != None:
                v = row['cor1'].strip('(').strip(')').split(':')
                #print row['cor1'], v
                obj.icores.append((int(v[0]),int(v[1])))
            if row['cor2'] != None:
                v = row['cor2'].strip('(').strip(')').split(':')
                #print row['cor2'], v
                obj.icores.append((int(v[0]),int(v[1])))
            self.robos.append(obj)
    def lista_robos(self):
        tstr = ''
        for robo in self.robos:
            tstr += '%s %s'%(robo.id,robo.nome)
            for cor in robo.icores:
                tstr += ' (%d:%d) '%(cor[0],cor[1])
            tstr += '\n'
        return tstr
    def _salva_init(self):
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


    def atualiza_icores(self):
        self.icores = []
        for lcor in self.lcores:
             max = np.max(lcor)
             min = np.min(lcor)
             self.icores.append((min,max))
    def salva_str(self):
        tstr = '%s,%s'%(self.id,self.nome)
        for cores in self.icores:
            tstr += ',(%d:%d)'%(cores[0],cores[1])
        return tstr
