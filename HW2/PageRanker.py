from math import log2
from collections import defaultdict

class PageRanker(object):

    def readGraph(self, inputFilename):
        self.inLinks = defaultdict(list)
        self.outCount = defaultdict(int)
        with open(inputFilename, 'r') as inputFile:
            for line in inputFile:
                docs = line.rstrip('\n').split(' ')
                doc, inLinks = docs[0], docs[1:]
                for inLink in inLinks:
                    self.inLinks[doc].append(inLink)
                    self.outCount[inLink] += 1
        self.docs = self.inLinks.keys()
        self.N = len(self.docs)
        self.dangling = [doc for doc in self.docs if self.outCount[doc] == 0]
        # print(self.dangling)
        return self.inLinks

    def getPerplexity(self, pr):
        h = 0.0
        for doc in self.docs:
            p = pr[doc]
            h -= p * log2(p)
        return 2 ** h

    def converged(self, pr):
        self.perplexity.append(self.getPerplexity(pr))
        l = len(self.perplexity)
        if l < 5:
            return False
        for i in range(l - 4, l):
            if abs(self.perplexity[i] - self.perplexity[i - 1]) >= 1.0:
                return False
        return True

    def compute(self, d=0.85, maxIter=None):
        self.perplexity = []
        pr = {}
        for doc in self.docs:
            pr[doc] = 1.0 / self.N
        while not self.converged(pr):
            if maxIter and len(self.perplexity) > maxIter:
                break
            newPR = {}
            sinkPR = 0
            for doc in self.dangling:
                sinkPR += pr[doc]
            for doc in self.docs:
                newPR[doc] = (1 - d) / self.N
                newPR[doc] += d * sinkPR / self.N
                for inLink in self.inLinks[doc]:
                    newPR[doc] += d * pr[inLink] / self.outCount[inLink]
            pr = newPR
        self.pr = pr
        return pr

    def outputTopK(self, k, filename):
        result = sorted(self.pr.items(), key=lambda x: -x[1])[:k]
        with open(filename, 'w+') as fout:
            for docID, pr in result:
                fout.write(str(pr) + "\t" + docID + '\n')

    def outputPerplexity(self, filename):
        with open(filename, 'w+') as fout:
            for p in self.perplexity:
                fout.write(str(p) + '\n')

    def rankByInLinkCount(self):
        self.pr = {}
        for doc in self.docs:
            self.pr[doc] = len(self.inLinks[doc])


if __name__ == "__main__":
    pr = PageRanker()
    inputFilename = input("Enter the graph filename: ")
    pr.readGraph(inputFilename)

    # Run one of the following 4 lines, comment out the others
    pr.compute()                # baseline: d = 0.85
    # pr.compute(d=.55)           # d = 0.55
    # pr.compute(maxIter=4)       # iteration = 4
    # pr.rankByInLinkCount()      # rank by in-link count

    k = int(input("Enter top k results to output: k = "))
    rankingFile = input("Enter the ranking output filename: ")
    pr.outputTopK(k, rankingFile)

    if hasattr(pr, "perplexity"):
        perplexityFile = input("Enter the perplexity output filename: ")
        pr.outputPerplexity(perplexityFile)