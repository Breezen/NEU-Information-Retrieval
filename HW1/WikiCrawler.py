import re, requests
from bs4 import BeautifulSoup
from time import sleep

WIKI = "https://en.wikipedia.org"

class WikiCrawler(object):

    def __init__(self, seedURL, keywords=None, max=1000, depth=6, wait=1):
        self.seedURL = seedURL      # starting URL
        self.keywords = [keyword.lower() for keyword in keywords] if keywords else None
        self.max = max              # max # of links to get
        self.depth = depth          # max depth to crawl
        self.wait = wait            # seconds to wait between each GET request

    def getLinks(self, URL):
        # delay to respect the the politeness policy
        sleep(self.wait)
        # use requests to get response from Wiki
        res = requests.get(URL)
        if res.status_code != requests.codes.ok or res.is_redirect:
            return []
        # use BeautifulSoup to parse the response body
        body = BeautifulSoup(res.content, "html.parser").find(id="bodyContent")
        links = []
        for href in body.find_all("a"):
            link = href.get("href")
            if link and re.match('/wiki/.*', link) is not None \
                    and re.match('/wiki/Main_Page', link) is None \
                    and re.match('/wiki/(.*)#(.*)', link) is None \
                    and re.match('/wiki/(.*):(.*)', link) is None:
                if self.keywords is not None and not self.containsKeyword(link, href.string):
                    continue
                links.append(WIKI + link)
        return links

    def containsKeyword(self, URL, text):
        for keyword in self.keywords:
            if URL.lower().find(keyword) != -1 or (text and text.lower().find(keyword) != -1):
                return True
        return False

    def BFS(self):
        num = 1
        self.result = [self.seedURL]
        depth = {self.seedURL: 1}
        for URL in self.result:
            # limit the depth
            if depth[URL] > self.depth:
                print("maximum depth reached: ", self.depth)
                return
            links = self.getLinks(URL)
            for link in links:
                if link not in depth:
                    depth[link] = depth[URL] + 1
                    self.result.append(link)
                    num += 1
                    if num >= self.max:
                        print("maximum depth reached: ", depth[link])
                        return

    def DFS_Imp(self, URL, depth):
        self.maxdepth = max(depth, self.maxdepth)
        self.result.append(URL)
        self.visited[URL] = True
        if len(self.result) >= self.max:
            return
        if depth < self.depth:
            for link in self.getLinks(URL):
                if len(self.result) < self.max and link not in self.visited:
                    self.DFS_Imp(link, depth + 1)

    def DFS(self):
        self.result = []
        self.visited = {self.seedURL: True}
        self.maxdepth = 1
        self.DFS_Imp(self.seedURL, 1)
        print("maximum depth reached: ", self.maxdepth)

    def saveResult(self, fileName):
        file = open(fileName, "w")
        for link in self.result:
            file.write(link + '\n')
        file.close()

if __name__ == "__main__":
    seedURL = input("Please enter a seed URL: ")
    keywords = input("Please enter keywords for focused crawling (split by a single space): ").split(' ')

    crawler = WikiCrawler(seedURL)

    print("Task1 BFS:")
    crawler.BFS()
    crawler.saveResult("T1_BFS.txt")

    print("Task1 DFS:")
    crawler.DFS()
    crawler.saveResult("T1_DFS.txt")

    print("Focused BFS:")
    focusedCrawler = WikiCrawler(seedURL, keywords=keywords)
    focusedCrawler.BFS()
    focusedCrawler.saveResult("T2_BFS.txt")