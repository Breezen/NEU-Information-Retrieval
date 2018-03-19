import wikipedia

class CorpusGenerator:
    def __init__(self, wikiTitle):
        self.title = wikiTitle
        self.content = wikipedia.page(wikiTitle).content

    def parse(self, caseFolding=True, removePunc=True):
        if caseFolding:
            self.content = self.content.casefold()
        if removePunc:
            pass

    def save(self):
        with open("corpus/" + self.title + ".txt", "w+") as fout:
            fout.write(self.content)

if __name__ == "__main__":
    cg = CorpusGenerator("Solar_eclipse")
    cg.parse()
    cg.save()