import os

if not os.path.exists("statistics"):
    os.mkdir("statistics")

for n in 1, 2, 3:
    file = "index/freq" + str(n) + ".txt"
    with open(file, 'r') as fin:
        index = eval(fin.read())
    tf, df = {}, {}
    for term, records in index.items():
        df[term] = len(records)
        count = 0
        for doc, cnt in records:
            count += cnt
        tf[term] = count
    # Generate tf and df tables
    with open("statistics/termFreq" + str(n) + ".txt", "w+") as fout:
        tf = sorted(tf.items(), key=lambda x: x[1], reverse=True)
        for term, freq in tf:
            fout.write(str(term) + ":\t" + str(freq) + '\n')
    with open("statistics/docFreq" + str(n) + ".txt", "w+") as fout:
        df = sorted(df.items())
        for term, freq in df:
            fout.write(str(term) + ":\t" + str(freq) + '\n')
            for doc, cnt in index[term]:
                fout.write(doc + '\n')