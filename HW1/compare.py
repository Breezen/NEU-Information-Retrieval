bfs = open('T1_BFS.txt', 'r')
dfs = open('T1_DFS.txt', 'r')

hash = {}

for link in bfs:
    hash[link] = True

count = 0
for link in dfs:
    if link in hash:
        count += 1

print(count)

bfs.close()
bfs.close()