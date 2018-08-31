"""."""
import re
import w3lib.html
import requests
import nltk
import pandas as pd


def clean(rawdata):
    r"""清洗原文.

    去除数字字符占比超过%25的tbale
    去除所有tag
    html entity 转义
    替换\xa0
    """
    while True:
        # table = re.search('<table(?!.*<table).*?</table>', rawdata)
        table = re.search('<table.*?</table>', rawdata)
        if not table:
            break
        # import pdb; pdb.set_trace()
        table = w3lib.html.replace_tags(table.group(), ' ')
        table = w3lib.html.replace_entities(table)
        table = re.sub('\xa0', ' ', table)
        nLen = len(re.findall('\d', table))
        cLen = len(re.findall('\w', table))
        if cLen != 0 and nLen/cLen > 0.25:
            table = ''
        # rawdata = re.sub('<table(?!.*<table).*?</table>', table, rawdata, 1)
        rawdata = re.sub('<table.*?</table>', table, rawdata, 1)
    rawdata = w3lib.html.replace_tags(rawdata, ' ')
    rawdata = w3lib.html.replace_entities(rawdata)
    rawdata = re.sub('\xa0', ' ', rawdata)
    return rawdata


def freq(content):
    """.

    对于每个文档，我们使用所有句子并使用总体不确定性，风险和歧义单词列表构建单词计数。
    作为文件长度的度量，我们计算完整的Loughran和McDonald（2011）词典中出现的句子和单词的数量。
    """
    sentences = nltk.sent_tokenize(content)
    results = list()
    for sent in sentences:
        words_new = list()
        words = nltk.word_tokenize(sent)
        for word in words:
            if len(word) > 1 and word.isalpha():
                words_new.append(word.upper())
        if len(words_new) > 0:
            results.append(nltk.FreqDist(words_new))
    return results


def count(freqs):
    """.

    计算频率
    uncertainty/McDonald
    Ambiguity/McDonald
    Risk/McDonald
    Ambiguity_sent/sentences
    Risk_sent/sentences
    negative/McDonald
    positive/McDonald
    """
    Sentences = len(freqs)
    Uncertainty = 0
    McDonald = 0
    Ambiguity = 0
    Risk = 0
    Ambiguity_sent = 0
    Risk_sent = 0
    Negative = 0
    Positive = 0
    for record in freqs:
        flag_risk = 0
        flag_ambiguity = 0
        for word in risk_list:
            i = record.get(word)
            if i:
                Risk += i
                Uncertainty += i
                if flag_risk == 0:
                    Risk_sent += 1
                    flag_risk = 1
        for word in ambiguity_list:
            i = record.get(word)
            if i:
                Ambiguity += i
                Uncertainty += i
                if flag_ambiguity == 0:
                    Ambiguity_sent += 1
                    flag_ambiguity = 1
        for word in uncertainty_list:
            Uncertainty += record.get(word, 0)
        for word in mcDonald_list:
            McDonald += record.get(word, 0)
        for word in negative_list:
            Negative += record.get(word, 0)
        for word in positive_list:
            Positive += record.get(word, 0)
    result = dict()
    result['Uncertainty_McDonald'] = round(Uncertainty/McDonald, 4)
    result['Ambiguity_McDonald'] = round(Ambiguity/McDonald, 4)
    result['Risk_McDonald'] = round(Risk/McDonald, 4)
    result['Ambiguity_sent_Sentences'] = round(Ambiguity_sent/Sentences, 4)
    result['Risk_sent_Sentences'] = round(Risk_sent/Sentences, 4)
    result['Negative_McDonald'] = round(Negative/McDonald, 4)
    result['Positive_McDonald'] = round(Positive/McDonald, 4)
    return result


global risk_list
global ambiguity_list
global uncertainty_list
global mcDonald_list
global negative_list
global positive_list


if __name__ == '__main__':
    """."""
    f = open('demand20180810/risk.txt')
    risk_list = list(l.strip() for l in f.readlines())
    f = open('demand20180810/ambiguity.txt')
    ambiguity_list = list(l.strip() for l in f.readlines())
    f = open('demand20180810/uncertainty.txt')
    uncertainty_list = list(l.strip() for l in f.readlines())
    f = open('demand20180810/negative.txt')
    negative_list = list(l.strip() for l in f.readlines())
    f = open('demand20180810/positive.txt')
    positive_list = list(l.strip() for l in f.readlines())
    df = pd.read_excel('demand20180810/LoughranMcDonald_MasterDictionary_2016.xlsx', usecols=0)
    mcDonald_list = list(df['Word'])

    url = "https://www.sec.gov/Archives/edgar/data/1590714/000159071418000033/pah10-k20171231document.htm"
    r = requests.get(url)
    content = clean(r.text)
    print('清洗完成！')
    freqs = freq(content)
    print('计算每个句子的单词频率完成！')
    result = count(freqs)
    print(result)
