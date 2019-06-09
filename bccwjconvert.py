import math

from readkanji import *

def katakana_to_hiragana(katakana):
    ah = ord('あ')
    ak = ord('ア')
    diff = ak - ah
    txt = ''
    for c in list(katakana):
        txt += chr(ord(c)-diff)

    return txt

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def apply_position_weight_curve(n):
    college_level = 40000

# l = [x * x for x in range(150)]
# print(l)
# 
# cap = 1000
# max_value = cap*cap
# max_exp = max_value * max_value
# max_cube = max_value * max_value * max_value
# 
# 
# for n in [x * x for x in range(1,cap)]:
#     print(n,
#           '{:.2f}'.format(min(n/max_value,1.0)),
#           '{:.2f}'.format(min(n*n/max_exp,1.0)),
#           '{:.2f}'.format(min(n*n*n/max_cube,1.0))
#     )
# 
# print(l)
# exit()


path = 'bccwj_frequencylist.tsv'
count = 0
with open(path) as f:
    next(f)
    for line in f:
        count += 1


c = 0

center = count/2
width = count

max_log = math.log2(count)*0.75

kr = KanjiReader()

with open(path) as f:
    next(f)
    for line in f:
        c += 1
        s = line.split('\t')

        curved_weight = min([math.log2(c)/max_log,1])
        kanji_difficulty = kr.get_sentence_difficulty(s[2])

        # all weights are between 0-1
        weights = [curved_weight, kanji_difficulty]
        combined = sum(weights)/len(weights)

        difficulty = "{:.2f}".format(combined)
        print(c,difficulty,s[2],katakana_to_hiragana(s[1]))

