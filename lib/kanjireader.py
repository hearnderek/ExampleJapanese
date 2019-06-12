import re

class KanjiReader:
    kanji_levels = {}
    hardest_level = 8

    def __init__ (self):
        #init
        with open('kanji.txt') as fp:
            for line in fp:
                number = int(line[0])
                kanji = line[2:].strip().split(' ')
                for moji in kanji:
                    self.kanji_levels[moji]=int(number)

    def is_kanji(self, kanji):
        if type(kanji) is not str:
            return list(map(self.is_kanji, kanji))
        elif len(kanji) > 1:
            return list(map(self.is_kanji, list(kanji)))
        else:
            return bool(re.search('\w',kanji)) and not bool(re.search('[ーa-zA-Z\dあ-んア-ンヴ]',kanji))

    def get_kanji_level (self, kanji):
        if type(kanji) is not str:
            return list(map(self.get_kanji_level, kanji))
        elif len(kanji) > 1:
            return list(map(self.get_kanji_level, list(kanji)))
        elif self.is_kanji(kanji):
            return self.kanji_levels.get(kanji, self.hardest_level)
        else:
            return 0


    # Trying to figure out a way to judge difficulty of a sentence based on Kanji usage
    def get_sentence_difficulty (self, kanji_level_list, verbose=False):
        if type(kanji_level_list) is str:
            kanji_level_list = self.get_kanji_level(kanji_level_list)
        
        if type(kanji_level_list) is int:
            kanji_level_list = [kanji_level_list]

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
        kanji_average = sum(kanji) / kanji_len / self.hardest_level
        kanji_mean = kanji[int(kanji_len/2)] / self.hardest_level
        kanji_80_percentile = kanji[int(kanji_len*0.8)] / self.hardest_level
        kanji_max_percentage = kanji_max / self.hardest_level

        if verbose:
            d = {
                "kp":kanji_percentage,
                "ka":kanji_average,
                "km":kanji_mean,
                "k8p":kanji_80_percentile,
                "kmp":kanji_max_percentage,
                "kanji":kanji_level_list
            }
            print(d)

        metrics = [kanji_percentage, kanji_average, kanji_mean, kanji_80_percentile, kanji_max_percentage]
        return sum(metrics)/len(metrics)
    

    def sentence_test (self, sentence, verbose=False):
        level = self.get_kanji_level(sentence)
        difficulty = self.get_sentence_difficulty(level, verbose)
        print(sentence)
        print(difficulty)

    def test ():
        test = '私'
        l = self.get_kanji_level(test)
        d = self.get_sentence_difficulty([l])
        print(len(test))
        print(l)
        print(d)

        test2 = '私と友達を:。、！'
        l1 = self.get_kanji_level(test2)
        d1 = self.get_sentence_difficulty(l1)
        print(len(test2))
        print(l1)
        print(d1)

        test3 = '岩手県大槌町の工事現場で今年2月に見つかった遺骨は、東日本大震災で行方不明になっていた大槌町の女性であることがわかりました。'
        test4 = 'Amazon Cashはスマートフォンの画面に専用バーコードを表示させて、店頭のレジで支払った金額をそのままAmazonアカウントに自動追加（チャージ）できるサービス。'
        test5 = '開発はこれまでのシリーズとは異なるスタッフにより新規に編成されたプロジェクトチーム・メルフェスにより行われ、様々な違いから従来作とは全体的な雰囲気を異なるものとしている'
        test6 = '戦闘シーンやフィールドなどのグラフィックは3Dで描かれており、移動中・戦闘中のキャラクターのグラフィックは4頭身ほどにデフォルメされている。'
        test7 = '介護保険制度とは、介護が必要となった方やそのご家族を社会全体で支えていく仕組みです。'
        test8 = '当行はお客さまへの情報提供の一環として、外国為替相場に関する相場見通し等のレポートをご提供する場合があります。'
        test9 = '遺跡船へ漂着した直後、シャーリィは山賊の首領にして魔獣使いのモーゼス・シャンドルに捕まる。'
        test10 = 'ありがとう'
        test11 = '1940年9月7日、ローマに生まれる。'
        test12 = 'スマートフォ'
        test13 = 'イタリアのヴェネツィアに生まれ、オーストリアのウィーンで没した。'
        test14 = 'ロレーヌのバドンヴィレに生まれる'
        self.sentence_test(test3)
        self.sentence_test(test4)
        self.sentence_test(test5)
        self.sentence_test(test6)
        self.sentence_test(test7)
        self.sentence_test(test8)
        self.sentence_test(test9)
        self.sentence_test(test10)
        self.sentence_test(test11)
        self.sentence_test(test12)
        self.sentence_test(test13)
        self.sentence_test(test14)


