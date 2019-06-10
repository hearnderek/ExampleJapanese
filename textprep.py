""" This reads in a Japanese txt file and splits the sentences onto their own lines then gives each sentence a difficulty """

import re
import sys
from readkanji import KanjiReader

# Read from specified file
file = sys.argv[1]

# main
with open(file) as fp:

    kr = KanjiReader()

    for line in fp:
        # Splitting up the wikipedia file so each sentence is on its own line
        # TODO don't split up 。[」]sentences
        x = line.replace('。','。\n').strip()
        if x != '':
            # if the file was already parsed by this script remove the old score
            if re.search(r'^\d.\d\d:', x):
                    x = x[5:]

            # append a difficulty score to the sentence
            difficulty = kr.get_sentence_difficulty(line)
            print("{:.2f}:{}".format(difficulty,x))
