import re
import sys

print("Processing: " + sys.argv[1])
file = sys.argv[1]

with open(file) as fp:
    for line in fp:
        x = line.replace('。','。\n').strip()
        if x != '':
            print(x)
