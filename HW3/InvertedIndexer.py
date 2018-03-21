import os, re
import collections

class InvertedIndexer:
    def __init__(self, inputDir):
        self.content = {}
        self.words = {}
        for file in os.listdir(inputDir):
            if file != ".DS_Store":
                with open(inputDir + '/' + file, 'r') as fin:
                    content = fin.read()
                    file = file.rstrip(".txt")
                    self.content[file] = content
                    self.words[file] = content.split()

    def indexNTerms(self, n=1):
        count = {}
        for file, words in self.words.items():
            terms = zip(*[words[i:] for i in range(n)])
            count[file] = len(set(terms))
        return count

    def indexFreq(self, n=1):
        index = collections.defaultdict(list)
        for file, words in self.words.items():
            terms = zip(*[words[i:] for i in range(n)])
            count = collections.Counter(terms)
            for term, cnt in count.items():
                index[term].append((file, cnt))
        return dict(index)

    def indexPos(self):
        index = collections.defaultdict(list)
        for file, words in self.words.items():
            for w in set(words):
                for pos in re.finditer(w, self.content[file]):
                    index[w].append((file, pos.start()))
        return dict(index)

if __name__ == "__main__":
    indexer = InvertedIndexer("corpus")

    if not os.path.exists("index"):
        os.mkdir("index")

    for n in 1, 2, 3:
        with open("index/nterms" + str(n) + ".txt", "w+") as fout:
            fout.write(str(indexer.indexNTerms(n)))
        with open("index/freq" + str(n) + ".txt", "w+") as fout:
            fout.write(str(indexer.indexFreq(n)))

    with open("index/pos1.txt", "w+") as fout:
        fout.write(str(indexer.indexPos()))