#!/usr/bin/env python3
"""Translate unidic-mecab to english"""
import re
import os
from collections import OrderedDict

TRANSLATIONS = {
    'inflection_type': {
        'カ行変格': 'irreg.kuru',
        'サ行変格': 'irreg.suru',
        '上一段-ア行': 'ichidan',
        '上一段-カ行': 'ichidan',
        '上一段-ガ行': 'ichidan',
        '上一段-ザ行': 'ichidan',
        '上一段-タ行': 'ichidan',
        '上一段-ナ行': 'ichidan',
        '上一段-ハ行': 'ichidan',
        '上一段-バ行': 'ichidan',
        '上一段-マ行': 'ichidan',
        '上一段-ラ行': 'ichidan',
        '下一段-ア行': 'ichidan',
        '下一段-カ行': 'ichidan',
        '下一段-ガ行': 'ichidan',
        '下一段-サ行': 'ichidan',
        '下一段-ザ行': 'ichidan',
        '下一段-タ行': 'ichidan',
        '下一段-ダ行': 'ichidan',
        '下一段-ナ行': 'ichidan',
        '下一段-ハ行': 'ichidan',
        '下一段-バ行': 'ichidan',
        '下一段-マ行': 'ichidan',
        '下一段-ラ行': 'ichidan',
        '五段-カ行': 'godan',
        '五段-ガ行': 'godan',
        '五段-サ行': 'godan',
        '五段-タ行': 'godan',
        '五段-ナ行': 'godan',
        '五段-バ行': 'godan',
        '五段-マ行': 'godan',
        '五段-ラ行': 'godan',
        '五段-ワア行': 'godan',
        '助動詞-ジャ': 'aux-ja',
        '助動詞-タ': 'aux-ta',
        '助動詞-タイ': 'aux-tai',
        '助動詞-ダ': 'aux-da',
        '助動詞-デス': 'aux-desu',
        '助動詞-ドス': 'aux-dosu',
        '助動詞-ナイ': 'aux-nai',
        '助動詞-ナンダ': 'aux-nanda',
        '助動詞-ヌ': 'aux-nu',
        '助動詞-ヘン': 'aux-hen',
        '助動詞-マイ': 'aux-mai',
        '助動詞-マス': 'aux-masu',
        '助動詞-ヤ': 'aux-ya',
        '助動詞-ヤス': 'aux-yasu',
        '助動詞-ラシイ': 'aux-rashii',
        '助動詞-レル': 'aux-reru',
        '形容詞': 'i.adj',
        '文語カ行変格': 'lit.irreg.kuru',
        '文語サ行変格': 'lit.irreg.suru/su',
        '文語ナ行変格': 'lit.irreg.nu',
        '文語ラ行変格': 'lit.irreg.ru',
        '文語上一段-ナ行': 'lit.ichidan',
        '文語上一段-マ行': 'lit.ichidan',
        '文語上一段-ワ行': 'lit.ichidan',
        '文語上二段-ガ行': 'lit.nidan',
        '文語上二段-タ行': 'lit.nidan',
        '文語上二段-ダ行': 'lit.nidan',
        '文語上二段-ハ行': 'lit.nidan',
        '文語上二段-バ行': 'lit.nidan',
        '文語上二段-マ行': 'lit.nidan',
        '文語上二段-ヤ行': 'lit.nidan',
        '文語上二段-ラ行': 'lit.nidan',
        '文語下一段-カ行': 'lit.ichidan',
        '文語下二段-ア行': 'lit.nidan',
        '文語下二段-カ行': 'lit.nidan',
        '文語下二段-ガ行': 'lit.nidan',
        '文語下二段-サ行': 'lit.nidan',
        '文語下二段-ザ行': 'lit.nidan',
        '文語下二段-タ行': 'lit.nidan',
        '文語下二段-ダ行': 'lit.nidan',
        '文語下二段-ナ行': 'lit.nidan',
        '文語下二段-ハ行': 'lit.nidan',
        '文語下二段-バ行': 'lit.nidan',
        '文語下二段-マ行': 'lit.nidan',
        '文語下二段-ヤ行': 'lit.nidan',
        '文語下二段-ラ行': 'lit.nidan',
        '文語下二段-ワ行': 'lit.nidan',
        '文語助動詞-キ': 'lit.aux-ki',
        '文語助動詞-ケム': 'lit.aux-kemu',
        '文語助動詞-ケリ': 'lit.aux-keri',
        '文語助動詞-ゴトシ': 'lit.aux-gotoshi',
        '文語助動詞-ザマス': 'lit.aux-zamasu',
        '文語助動詞-ザンス': 'lit.aux-zansu',
        '文語助動詞-ジ': 'lit.aux-ji',
        '文語助動詞-ズ': 'lit.aux-zu',
        '文語助動詞-タリ-完了': 'lit.aux-tari',
        '文語助動詞-タリ-断定': 'lit.aux-tari',
        '文語助動詞-ツ': 'lit.aux-tsu',
        '文語助動詞-ナリ-伝聞': 'lit.aux-nari',
        '文語助動詞-ナリ-断定': 'lit.aux-nari',
        '文語助動詞-ヌ': 'lit.aux-nu',
        '文語助動詞-ベシ': 'lit.aux-beshi',
        '文語助動詞-マジ': 'lit.aux-maji',
        '文語助動詞-ム': 'lit.aux-mu',
        '文語助動詞-ラシ': 'lit.aux-rashi',
        '文語助動詞-ラム': 'lit.aux-ramu',
        '文語助動詞-リ': 'lit.aux-ri',
        '文語助動詞-ンス': 'lit.aux-nsu',
        '文語四段-カ行': 'lit.yodan',
        '文語四段-ガ行': 'lit.yodan',
        '文語四段-サ行': 'lit.yodan',
        '文語四段-タ行': 'lit.yodan',
        '文語四段-ハ行': 'lit.yodan',
        '文語四段-バ行': 'lit.yodan',
        '文語四段-マ行': 'lit.yodan',
        '文語四段-ラ行': 'lit.yodan',
        '文語形容詞': 'lit.i-adj',
        '文語形容詞-ク': 'lit.i-adj-ku',
        '文語形容詞-シク': 'lit.i-adj-shiku',
        '無変化型': 'non.inflecting'
    },
    'inflection_form': {
        'ク語法': 'ku.noun',
        '仮定形-一般': 'hypothetical',
        '仮定形-融合': 'hypothetical-agglut.',
        '命令形': 'imperative',
        '已然形-一般': 'realis',
        '已然形-補助': 'realis',
        '意志推量形': 'volitional',
        '未然形-サ': 'irrealis',
        '未然形-セ': 'irrealis',
        '未然形-一般': 'irrealis',
        '未然形-撥音便': 'irrealis-nasal',
        '未然形-補助': 'irrealis',
        '終止形-ウ音便': 'terminal-u',
        '終止形-一般': 'terminal',
        '終止形-促音便': 'terminal-nasal',
        '終止形-撥音便': 'terminal-nasal',
        '終止形-融合': 'terminal-agglut.',
        '終止形-補助': 'terminal',
        '語幹-サ': 'stem',
        '語幹-一般': 'stem',
        '連体形-イ音便': 'attributive-i',
        '連体形-ウ音便': 'attributive-u',
        '連体形-一般': 'attributive',
        '連体形-一般+送り仮名省略': 'attributive-okuri.abbr.',
        '連体形-撥音便': 'attributive-nasal',
        '連体形-省略': 'attributive-abbr.',
        '連体形-補助': 'attributive',
        '連用形-イ音便': 'continuative-i',
        '連用形-イ音便+送り仮名省略': 'continuative-i+okuri.abbr.',
        '連用形-ウ音便': 'continuative-u',
        '連用形-キ接続': 'continuative-ki.conn.',
        '連用形-ト': 'continuative-to',
        '連用形-ニ': 'continuative-ni',
        '連用形-一般': 'continuative',
        '連用形-一般+送り仮名省略': 'continuative-okuri.abbr.',
        '連用形-促音便': 'continuative-nasal',
        '連用形-撥音便': 'continuative-nasal',
        '連用形-省略': 'continuative-abbr.',
        '連用形-融合': 'continuative-agglut.',
        '連用形-補助': 'continuative',
    },
    'pos': {
        '代名詞': 'pronoun',
        '副詞': 'adverb',
        '助動詞': 'aux. verb',
        '助詞': 'particle',
        '動詞': 'verb',
        '名詞': 'noun',
        '形容詞': 'i.adjective',
        '形状詞': 'na.adjective',
        '感動詞': 'interjection',
        '接尾辞': 'suffix',
        '接続詞': 'conjunction',
        '接頭辞': 'prefix',
        '空白': 'blank',
        '補助記号': 'symbol',
        '記号': 'symbol',
        '連体詞': 'prenoun'
    },
    'pos2': {
        'タリ': 'tari',
        'フィラー': 'filler',
        '一般': 'ordinary',
        '係助詞': 'binding',
        '副助詞': 'adverbial',
        '助動詞語幹': 'aux.stem',
        '動詞的': 'verbal',
        '句点': 'period',
        '名詞的': 'substantive',
        '固有名詞': 'proper',
        '形容詞的': 'adjectival',
        '形状詞的': 'adjectival',
        '括弧閉': 'closing.bracket',
        '括弧開': 'opening.bracket',
        '接続助詞': 'conjunctive',
        '数詞': 'numeral',
        '文字': 'character',
        '普通名詞': 'common',
        '格助詞': 'case',
        '準体助詞': 'acts.on.the.whole.phrase',
        '終助詞': 'final',
        '読点': 'comma',
        '非自立可能': 'non.independent?',
        'ＡＡ': 'ＡＡ'
    },
    'pos3': {
        'サ変可能': 'irreg.suru/su?',
        'サ変形状詞可能': 'irreg.suru/su.adj.?',
        '一般': 'ordinary',
        '人名': 'person',
        '副詞可能': 'adverb?',
        '助数詞': 'counter',
        '助数詞可能': 'counter?',
        '地名': 'place',
        '形状詞可能': 'adjective?',
        '顔文字': 'emoticon'
    },
    'pos4': {
        '一般': 'ordinary',
        '名': 'given',
        '国': 'country',
        '姓': 'family'
    }
}

ENTRY_FORMAT = [
    '0',
    '1',
    '2',
    '3',
    'pos',
    'pos2',
    'pos3',
    'pos4',
    'inflection_type',
    'inflection_form',
    'lemma_reading',
    '11',
    '12',
    '13',
    '14',
    'orth_reading',
    '15',
    '16',
    '17',
    '18',
    '19',
]

def entry(line):
    """Split csv line and return a dictionary"""
    return OrderedDict(zip(ENTRY_FORMAT, line.split(',')))

def remove_chouon(text):
    """Remove long vowel marks from katakana text"""
    if not text:
        return ''
    output = []
    previous = ''
    for char in text:
        if char == 'ー':
            if previous in 'アカガサザタダナハバパマヤャラワ':
                output.append('ア')
            elif previous in 'イキギシジチヂニヒビピミリヰエケゲセゼテデネヘベペメレヱ':
                output.append('イ')
            elif previous in 'ウクグスズツヅヌフブプムユュルオコゴソゾトドノホボポモヨョロヲ':
                output.append('ウ')
            else:
                output.append('ー')
        else:
            output.append(char)
        previous = char
    return ''.join(output)

def main():
    """Read lex-original.csv and write a translated version to lex.csv"""

    ichidan_eru = re.compile(r'^下一段')

    lex_original = open('lex-original.csv', encoding='utf-8')
    try:
        os.remove('lex.csv')
    except FileNotFoundError:
        pass
    lex_translated = open('lex.csv', 'a', encoding='utf-8')

    potential = False
    for line in lex_original:
        potential = False
        line = entry(line)

        if (ichidan_eru.match(line['inflection_type'])
                and line['orth_reading']
                and line['lemma_reading'][-2:]
                != remove_chouon(line['orth_reading'][-2:])):
            line['inflection_type'] = 'potential'
            potential = True

        for key in line:
            if potential and key == 'inflection_type':
                continue
            try:
                line[key] = TRANSLATIONS[key][line[key]]
            except KeyError:
                pass

        lex_translated.write(','.join(line.values()))

    lex_original.close()
    lex_translated.close()

if __name__ == '__main__':
    main()
