import wikipedia

seedTitle = "Solar eclipse"
num = 1
result = [seedTitle]
visited = {seedTitle}

for title in result:
    links = wikipedia.page(title).links
    for link in links:
        if link.casefold() not in visited \
                and link.lower().find("disambiguation") == -1:
            visited.add(link.casefold())
            result.append(link)
            num += 1
            if num >= 1000:
                with open("BFS.txt", "w+") as fout:
                    for link in result:
                        fout.write(link + '\n')
                quit(0)