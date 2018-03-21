import os, string, wikipedia

class CorpusGenerator:
    def __init__(self, wikiTitle):
        self.title = wikiTitle
        page = wikipedia.page(wikiTitle)
        self.content = page.content

    def usefulForDigits(self, c, last, next):
        if next is None or next == ' ' or next == '\n':
            if last in string.digits:
                return c in "%"
            return False
        if next in string.digits and last in string.digits:
            return c in ",./"
        return False

    def parse(self, caseFolding=True, removePunc=True):
        if caseFolding:
            self.content = self.content.casefold()
        if removePunc:
            parsed = ""
            for i, c in enumerate(self.content):
                if c in string.punctuation and c != '-' \
                    and not self.usefulForDigits(c, self.content[i - 1], self.content[i + 1] if i + 1 < len(self.content) else None):
                    continue
                parsed += c
            self.content = parsed

    def save(self):
        if not os.path.exists("corpus"):
            os.mkdir("corpus")
        with open("corpus/" + self.title + ".txt", "w+") as fout:
            fout.write(self.content)

if __name__ == "__main__":
    with open("BFS.txt", "r") as fin:
        for title in fin:
            title = title.rstrip('\n')
            cg = CorpusGenerator(title)
            cg.parse()
            cg.save()