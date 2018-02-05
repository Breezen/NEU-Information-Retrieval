import os, requests
from time import sleep

inputFile = input("Enter the input filename containing wiki links: ")
fin = open(inputFile, 'r')

if not os.path.exists("./htmls"):
    os.makedirs("./htmls")

for link in fin:
    sleep(1)
    title = link[30:][:-1] + ".txt"
    with open("./htmls/" + title, 'w+') as fout:
        fout.write(requests.get(link).text)

fin.close()