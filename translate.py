#!/usr/bin/env python3
"""Translate unidic-mecab to english"""
import re
import os
from collections import OrderedDict

TRANSLATIONS = {
    'inflection_type': {
        'カ行変格': 'irregular kuru',
        'サ行変格': 'irregular suru',
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
        '助動詞-ジャ': 'aux|ja',
        '助動詞-タ': 'aux|ta',
        '助動詞-タイ': 'aux|tai',
        '助動詞-ダ': 'aux|da',
        '助動詞-デス': 'aux|desu',
        '助動詞-ドス': 'aux|dosu',
        '助動詞-ナイ': 'aux|nai',
        '助動詞-ナンダ': 'aux|nanda',
        '助動詞-ヌ': 'aux|nu',
        '助動詞-ヘン': 'aux|hen',
        '助動詞-マイ': 'aux|mai',
        '助動詞-マス': 'aux|masu',
        '助動詞-ヤ': 'aux|ya',
        '助動詞-ヤス': 'aux|yasu',
        '助動詞-ラシイ': 'aux|rashii',
        '助動詞-レル': 'aux|reru',
        '形容詞': 'i-adjective',
        '文語カ行変格': 'literary irregular kuru',
        '文語サ行変格': 'literary irregular suru/su',
        '文語ナ行変格': 'literary irregular nu',
        '文語ラ行変格': 'literary irregular ru',
        '文語上一段-ナ行': 'literary ichidan',
        '文語上一段-マ行': 'literary ichidan',
        '文語上一段-ワ行': 'literary ichidan',
        '文語上二段-ガ行': 'literary nidan',
        '文語上二段-タ行': 'literary nidan',
        '文語上二段-ダ行': 'literary nidan',
        '文語上二段-ハ行': 'literary nidan',
        '文語上二段-バ行': 'literary nidan',
        '文語上二段-マ行': 'literary nidan',
        '文語上二段-ヤ行': 'literary nidan',
        '文語上二段-ラ行': 'literary nidan',
        '文語下一段-カ行': 'literary ichidan',
        '文語下二段-ア行': 'literary nidan',
        '文語下二段-カ行': 'literary nidan',
        '文語下二段-ガ行': 'literary nidan',
        '文語下二段-サ行': 'literary nidan',
        '文語下二段-ザ行': 'literary nidan',
        '文語下二段-タ行': 'literary nidan',
        '文語下二段-ダ行': 'literary nidan',
        '文語下二段-ナ行': 'literary nidan',
        '文語下二段-ハ行': 'literary nidan',
        '文語下二段-バ行': 'literary nidan',
        '文語下二段-マ行': 'literary nidan',
        '文語下二段-ヤ行': 'literary nidan',
        '文語下二段-ラ行': 'literary nidan',
        '文語下二段-ワ行': 'literary nidan',
        '文語助動詞-キ': 'literary aux|ki',
        '文語助動詞-ケム': 'literary aux|kemu',
        '文語助動詞-ケリ': 'literary aux|keri',
        '文語助動詞-ゴトシ': 'literary aux|gotoshi',
        '文語助動詞-ザマス': 'literary aux|zamasu',
        '文語助動詞-ザンス': 'literary aux|zansu',
        '文語助動詞-ジ': 'literary aux|ji',
        '文語助動詞-ズ': 'literary aux|zu',
        '文語助動詞-タリ-完了': 'literary aux|tari',
        '文語助動詞-タリ-断定': 'literary aux|tari',
        '文語助動詞-ツ': 'literary aux|tsu',
        '文語助動詞-ナリ-伝聞': 'literary aux|nari',
        '文語助動詞-ナリ-断定': 'literary aux|nari',
        '文語助動詞-ヌ': 'literary aux|nu',
        '文語助動詞-ベシ': 'literary aux|beshi',
        '文語助動詞-マジ': 'literary aux|maji',
        '文語助動詞-ム': 'literary aux|mu',
        '文語助動詞-ラシ': 'literary aux|rashi',
        '文語助動詞-ラム': 'literary aux|ramu',
        '文語助動詞-リ': 'literary aux|ri',
        '文語助動詞-ンス': 'literary aux|nsu',
        '文語四段-カ行': 'literary yodan',
        '文語四段-ガ行': 'literary yodan',
        '文語四段-サ行': 'literary yodan',
        '文語四段-タ行': 'literary yodan',
        '文語四段-ハ行': 'literary yodan',
        '文語四段-バ行': 'literary yodan',
        '文語四段-マ行': 'literary yodan',
        '文語四段-ラ行': 'literary yodan',
        '文語形容詞': 'literary i-adjective',
        '文語形容詞-ク': 'literary i-adjective|ku',
        '文語形容詞-シク': 'literary i-adjective|shiku',
        '無変化型': 'doesn\'t inflect'
    },
    'inflection_form': {
        'ク語法': 'ku-noun',
        '仮定形-一般': 'hypothetical',
        '仮定形-融合': 'hypothetical|agglutination',
        '命令形': 'imperative',
        '已然形-一般': 'realis',
        '已然形-補助': 'realis',
        '意志推量形': 'volitional',
        '未然形-サ': 'irrealis',
        '未然形-セ': 'irrealis',
        '未然形-一般': 'irrealis',
        '未然形-撥音便': 'irrealis|nasal',
        '未然形-補助': 'irrealis',
        '終止形-ウ音便': 'terminal|u',
        '終止形-一般': 'terminal',
        '終止形-促音便': 'terminal|nasal',
        '終止形-撥音便': 'terminal|nasal',
        '終止形-融合': 'terminal|agglutination',
        '終止形-補助': 'terminal',
        '語幹-サ': 'stem',
        '語幹-一般': 'stem',
        '連体形-イ音便': 'attributive|i',
        '連体形-ウ音便': 'attributive|u',
        '連体形-一般': 'attributive',
        '連体形-一般+送り仮名省略': 'attributive|okurigana omission',
        '連体形-撥音便': 'attributive|nasal',
        '連体形-省略': 'attributive|omission',
        '連体形-補助': 'attributive',
        '連用形-イ音便': 'continuative|i',
        '連用形-イ音便+送り仮名省略': 'continuative|i+okurigana omission',
        '連用形-ウ音便': 'continuative|u',
        '連用形-キ接続': 'continuative|ki-connection',
        '連用形-ト': 'continuative|to',
        '連用形-ニ': 'continuative|ni',
        '連用形-一般': 'continuative',
        '連用形-一般+送り仮名省略': 'continuative|okurigana omission',
        '連用形-促音便': 'continuative|nasal',
        '連用形-撥音便': 'continuative|nasal',
        '連用形-省略': 'continuative|omission',
        '連用形-融合': 'continuative|agglutination',
        '連用形-補助': 'continuative',
    },
    'pos': {
        '代名詞': 'pronoun',
        '副詞': 'adverb',
        '助動詞': 'aux-verb',
        '助詞': 'particle',
        '動詞': 'verb',
        '名詞': 'noun',
        '形容詞': 'i-adjective',
        '形状詞': 'na-adjective',
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
        '助動詞語幹': 'aux stem',
        '動詞的': 'verbal',
        '句点': 'period',
        '名詞的': 'substantive',
        '固有名詞': 'proper',
        '形容詞的': 'adjectival',
        '形状詞的': 'adjectival',
        '括弧閉': 'closing bracket',
        '括弧開': 'opening bracket',
        '接続助詞': 'conjunctive',
        '数詞': 'numeral',
        '文字': 'character',
        '普通名詞': 'common',
        '格助詞': 'case',
        '準体助詞': 'acts on the whole phrase',
        '終助詞': 'final',
        '読点': 'comma',
        '非自立可能': 'non independent?',
        'ＡＡ': 'ascii art'
    },
    'pos3': {
        'サ変可能': 'irregular suru/su?',
        'サ変形状詞可能': 'irregular suru/su adjective?',
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

LEX_ENTRY_FORMAT = [
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

ID_ENTRY_FORMAT = [
    'pos',
    'pos2',
    'pos3',
    'pos4',
    'inflection_type',
    'inflection_form',
    '6',
    '7',
    '8',
]

REWRITE_ENTRY_FORMAT = [
    'pos',
    'pos2',
    'pos3',
    'pos4',
    'REST',
]

UNK_ENTRY_FORMAT = [
    '0',
    '1',
    '2',
    '3',
    'pos',
    'pos2',
    'pos3',
    'pos4',
    '8',
    '9',
]

def lex_entry(line):
    """Split lex.csv line and return a dictionary"""
    return OrderedDict(zip(LEX_ENTRY_FORMAT, line.split(',')))

def id_entry(line):
    """1 代名詞,*,*,*,*,*,*,*,和 --> ['1', OrderedDict(...)]"""
    line = line.split(' ', 1)
    return line[0], OrderedDict(zip(ID_ENTRY_FORMAT, line[1].split(',')))

def rewrite_entry(line):
    """助詞,*,*,*,*,*,*,...,*,*,*,*,*,*,*,*,*	$1,$2,$3,$4,$5,$6,$9,$11,$13 -->
    OrderedDict(pos:助詞,pos2:*,pos3:*,pos4:*,REST:...)"""
    max_split = len(REWRITE_ENTRY_FORMAT) - 1
    return OrderedDict(zip(REWRITE_ENTRY_FORMAT, line.split(',', max_split)))

def unk_entry(line):
    """DEFAULT,5968,5968,3857,補助記号,一般,*,*,*,* --> OrderedDict(...)"""
    return OrderedDict(zip(UNK_ENTRY_FORMAT, line.split(',')))

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

def translate_lex():
    """Read lex.csv.original and write a translated version to lex.csv"""

    ichidan_eru = re.compile(r'^下一段')

    lex_original = open('lex.csv.original', encoding='utf-8')
    try:
        os.remove('lex.csv')
    except FileNotFoundError:
        pass
    lex_translated = open('lex.csv', 'a', encoding='utf-8')

    potential = False
    for line in lex_original:
        potential = False
        line = lex_entry(line)

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

def translate_id(input_filename, output_filename):
    """Read left-id.def.original or right-id.def.original
    and write a translated version to *-id.def"""

    id_original = open(input_filename, encoding='utf-8')

    try:
        os.remove(output_filename)
    except FileNotFoundError:
        pass
    id_translated = open(output_filename, 'a', encoding='utf-8')

    for line in id_original:
        number, line = id_entry(line)

        for key in line:
            try:
                line[key] = TRANSLATIONS[key][line[key]]
            except KeyError:
                pass

        id_translated.write('{} {}'.format(number, ','.join(line.values())))

    id_original.close()
    id_translated.close()

def translate_rewrite():
    """Read rewrite.def.original and write a translated version to rewrite.def"""

    rewrite_original = open('rewrite.def.original', encoding='utf-8')

    try:
        os.remove('rewrite.def')
    except FileNotFoundError:
        pass
    rewrite_translated = open('rewrite.def', 'a', encoding='utf-8')

    translate = False
    for line in rewrite_original:
        if line.strip() in ['[left rewrite]', '[right rewrite]']:
            translate = True
            rewrite_translated.write(line)
            continue
        elif not line.strip():
            translate = False

        if translate:
            line = rewrite_entry(line)

            for key in line:
                try:
                    line[key] = TRANSLATIONS[key][line[key]]
                except KeyError:
                    pass

            rewrite_translated.write(','.join(line.values()))
        else:
            rewrite_translated.write(line)

    rewrite_original.close()
    rewrite_translated.close()

def translate_unk():
    """Read unk.def.original and write a translated version to unk.def"""

    unk_original = open('unk.def.original', encoding='utf-8')

    try:
        os.remove('unk.def')
    except FileNotFoundError:
        pass
    unk_translated = open('unk.def', 'a', encoding='utf-8')

    for line in unk_original:
        line = unk_entry(line)
        for key in line:
            try:
                line[key] = TRANSLATIONS[key][line[key]]
            except KeyError:
                pass

        unk_translated.write(','.join(line.values()))

    unk_original.close()
    unk_translated.close()

def main():
    """Translate unidic-mecab"""
    translate_lex()
    translate_id('left-id.def.original', 'left-id.def')
    translate_id('right-id.def.original', 'right-id.def')
    translate_rewrite()
    translate_unk()

if __name__ == '__main__':
    main()
