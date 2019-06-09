import re
import sys

file = sys.argv[1]

kanji_levels = {}
hardest_level = 8

#init
with open('kanji.txt') as fp:
    for line in fp:
        number = int(line[0])
        kanji = line[2:].strip().split(' ')
        # TODO 1 switch use of dictionary to have the kanji be keys
        kanji_levels[number]=kanji


#functions
def is_kanji(kanji):
    if type(kanji) is not str:
        return list(map(is_kanji, kanji))
    elif len(kanji) > 1:
        return list(map(is_kanji, list(kanji)))
    else:
        return bool(re.search('\w',kanji)) and not bool(re.search('[ーa-zA-Z\dあ-んア-ンヴ]',kanji))

def get_kanji_level (kanji):
    if type(kanji) is not str:
        return list(map(get_kanji_level, kanji))
    elif len(kanji) > 1:
        return list(map(get_kanji_level, list(kanji)))
    elif is_kanji(kanji):
        # TODO 1 switch use of dictionary to have the kanji be keys
        for level in kanji_levels:
            if any(kanji in k for k in kanji_levels[level]):
                return int(level)
        return int(hardest_level)
    else:
        return 0


# Trying to figure out a way to judge difficulty of a sentence based on Kanji usage
def get_sentence_difficulty (kanji_level_list):
    # there are a lot of unnessicary passes through the array
    # this could be optimized by using a single for loop
    length = len(kanji_level_list)
    kanji = list(filter(lambda x: x>0, kanji_level_list))
    kanji.sort()
    kanji_len = len(kanji)
    if kanji_len == 0:
        return 0
    kanji_max = kanji[-1]

    # all are 0-1 floats and thus easier to combine to a 0-1 difficulty raiting
    kanji_percentage = kanji_len / length
    kanji_average = sum(kanji) / kanji_len / hardest_level
    kanji_mean = kanji[int(kanji_len/2)] / hardest_level
    kanji_80_percentile = kanji[int(kanji_len*0.8)] / hardest_level
    kanji_max_percentage = kanji_max / hardest_level
    metrics = [kanji_percentage, kanji_average, kanji_mean, kanji_80_percentile, kanji_max_percentage]
    return sum(metrics)/len(metrics)




# main
with open(file) as fp:
    for line in fp:
        x = line.replace('。','。\n').strip()
        if x != '':
            if re.search(r'^\d.\d\d:', x):
                    x = x[5:]
            difficulty = get_sentence_difficulty(get_kanji_level(line))
            print("{:.2f}:{}".format(difficulty,x))
