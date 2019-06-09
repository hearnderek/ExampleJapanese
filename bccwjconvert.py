import math

def katakana_to_hiragana(katakana):
    ah = ord('あ')
    ak = ord('ア')
    diff = ak - ah
    txt = ''
    for c in list(katakana):
        txt += chr(ord(c)-diff)

    return txt

path = 'bccwj_frequencylist.tsv'
count = 0
with open(path) as f:
    next(f)
    for line in f:
        count += 1

max_log = math.log2(count)*0.75

c = 0
with open(path) as f:
    next(f)
    for line in f:
        c += 1
        s = line.split('\t')
        curved_weight = min([math.log2(c)/max_log,1])
        difficulty = "{:.2f}".format(curved_weight)
        print(c,difficulty,s[2],katakana_to_hiragana(s[1]))

