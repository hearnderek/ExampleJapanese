import re
import sys
from readkanji import KanjiReader

file = sys.argv[1]

# main
with open(file) as fp:

    kr = KanjiReader()

    for line in fp:
        x = line.replace('。','。\n').strip()
        if x != '':
            if re.search(r'^\d.\d\d:', x):
                    x = x[5:]
            difficulty = kr.get_sentence_difficulty(line)
            print("{:.2f}:{}".format(difficulty,x))
