import os, re, collections
from bs4 import BeautifulSoup

class GraphBuilder(object):
    def __init__(self, dir):
        self.dir = dir
        self.docs = set(os.listdir(dir))
        if ".DS_Store" in self.docs:
            self.docs.remove(".DS_Store")
        self.graph = collections.defaultdict(list)

    def getLinks(self, docID):
        with open(self.dir + '/' + docID, 'r') as file:
            html = file.read().replace('\n', '')
            body = BeautifulSoup(html, "html.parser").find(id="bodyContent")
            links = set()
            for href in body.find_all("a"):
                link = href.get("href")
                if link and re.match('/wiki/.*', link) is not None \
                        and re.match('/wiki/Main_Page', link) is None \
                        and re.match('/wiki/(.*)#(.*)', link) is None \
                        and re.match('/wiki/(.*):(.*)', link) is None \
                        and link[6:] in self.docs:
                    links.add(link[6:])
            return links

    def build(self):
        for doc in self.docs:
            for link in self.getLinks(doc):
                if link != doc:
                    self.graph[link].append(doc)

    def output(self, filename):
        with open(filename, 'w+') as file:
            for doc, inlinks in self.graph.items():
                file.write(doc)
                for inlink in inlinks:
                    file.write(' ' + inlink)
                file.write('\n')


if __name__ == "__main__":
    inputDir = input("Enter the name of the directory containing wiki pages: ")
    gb = GraphBuilder(inputDir)
    gb.build()
    outputFile = input("Enter the output filename: ")
    gb.output(outputFile)