from collections import defaultdict

class PageRanker(object):
    def __init__(self, d=0.85, maxIter=None):
        self.d = d
        self.maxIter = maxIter

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

if __name__ == "__main__":
    pr = PageRanker()
    inputFilename = input("Enter the graph filename: ")
    pr.readGraph(inputFilename)