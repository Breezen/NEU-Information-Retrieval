from math import log
from os import listdir
from collections import Counter

SYSTEM_NAME = "OkapiNonStopNonStemCaseFolded"
K1 = 1.2
B = 0.75
K2 = 100
R = RI = 0

class BM25:
    def __init__(self, corpusDir="corpus", indexFile="index.txt"):
        self.readIndex(indexFile)
        self.readCorpus(corpusDir)

    def readIndex(self, filename):
        with open(filename, 'r') as fin:
            self.index = eval(fin.read())

    def readCorpus(self, dir):
        self.avglen = 0
        self.length = {}
        for file in listdir(dir):
            if file != ".DS_Store":
                with open(dir + '/' + file, 'r') as fin:
                    file = file.rstrip(".txt")
                    l = len(fin.read().split())
                    self.avglen += l
                    self.length[file] = l
        self.N = len(self.length)
        self.avglen /= self.N

    def getBM25(self, file, query):
        score = 0
        K = K1 * ((1 - B) + B * self.length[file] / self.avglen)
        for w in query.split():
            if w not in self.index or file not in self.index[w]:
                continue
            tf = self.index[w][file]
            qf = self.qt[w]
            ni = len(self.index[w])
            score += log(((RI+.5)/(R-RI+.5))/((ni-RI+.5)/(self.N-ni-R+RI+.5))*((K1+1)*tf)/(K+tf)*((K2+1)*qf)/(K2+qf))
        return score

    def search(self, ID, query):
        query = query.casefold()
        self.qt = Counter(query.split())
        ranking = []
        for file in self.length:
            ranking.append((file, self.getBM25(file, query)))
        ranking.sort(key=lambda x: x[1], reverse=True)
        with open(query + ".txt", "w+") as fout:
            for i, (file, score) in enumerate(ranking[:100]):
                fout.write(str(ID) + "\tQ0\t" + file.replace(' ', '_') + '\t' + str(i) + '\t' + str(score) + '\t' + SYSTEM_NAME + '\n')


if __name__ == "__main__":
    bm = BM25()
    while True:
        ID = input("Enter Query ID (Q to quit): ")
        if ID == 'Q':
            break
        query = input("Enter Query Text: ")
        bm.search(ID, query)