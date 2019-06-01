import re

kanji_levels = {}
hardest_level = 7

#init
with open('kanji.txt') as fp:
    for line in fp:
        number = line[0]
        kanji = line[2:].strip().split(' ')
        kanji_levels[number]=kanji


#functions
def is_kanji(kanji):
    if type(kanji) is not str:
        return list(map(is_kanji, kanji))
    elif len(kanji) > 1:
        return list(map(is_kanji, list(kanji)))
    else:
        return bool(re.search('\w',kanji)) and not bool(re.search('[a-zA-Zあ-んア-ン]',kanji))

def get_kanji_level (kanji):
    if type(kanji) is not str:
        return list(map(get_kanji_level, kanji))
    elif len(kanji) > 1:
        return list(map(get_kanji_level, list(kanji)))
    elif is_kanji(kanji):
        for level in kanji_levels:
            if any(kanji in k for k in kanji_levels[level]):
                print(level)
                return level
        print(hardest_level)
        return hardest_level
    else:
        return 0


test = '私'
test2 = '私と友達を:。、！'
l = get_kanji_level(test)
print(len(test))
print(l)
l1 = get_kanji_level(test2)
print(len(test2))
print(l1)
test3 = '私と友達を:。、！'
x = is_kanji(test3)
print(test3)
print(x)
print(bool(re.search('[a-zA-Zあ-んア-ン]','が')))
