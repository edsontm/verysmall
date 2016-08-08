import csv


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


class LIARobo():
    def __init__(self,id,nome):
        self.id = id
        self.nome = nome
        self.cor1 = None
        self.cor2 = None