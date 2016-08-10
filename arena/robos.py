import csv
import numpy as np


class LIATime():
    def __init__(self,nrobos = 4):
        self.nrobos = nrobos
        self.robos = []
        self._carrega_init()
    def _carrega_init(self):
        f = csv.DictReader(open('init.csv'),delimiter =',')
        for row in f:
            obj = LIARobo(row['id'],row['nome'])
            for tcor in ['cor1','cor2']:
                if row[tcor] != None:
                    v = row[tcor].strip('(').strip(')').split('#')
                    v0 = v[0].split(':')
                    v1 = v[1].split(':')
                    tcormin = np.array([int(v0[0]),int(v0[1]),int(v0[2])])
                    tcormax = np.array([int(v1[0]),int(v1[1]),int(v1[2])])
                    obj.icores.append((tcormin,tcormax))
            self.robos.append(obj)

    def lista_robos(self):
        tstr = ''
        for robo in self.robos:
            tstr += robo.salva_str()
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
            mcor = np.matrix(lcor)

            maxh = np.max(mcor[:,0])
            minh = np.min(mcor[:,0])

            maxs = np.max(mcor[:,1])
            mins = np.min (mcor[:, 1])

            maxv = np.max(mcor[:,2])
            minv = np.min (mcor[:, 2])

            tcormin = np.array([minh, mins, minv])
            tcormax = np.array([maxh,maxs,maxv])

            self.icores.append((tcormin,tcormax))
    def salva_str(self):
        tstr = '%s,%s'%(self.id,self.nome)
        for cores in self.icores:
            c0 = cores[0]
            c1 = cores[1]
            tstr += ',(%d:%d:%d#%d:%d:%d)'%(c0[0],c0[1],c0[2],c1[0],c1[1],c1[2])
        return tstr
