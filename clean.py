import re

def clean_file(rawdata):
    rawdata = re.sub('(\n)\s*', ' ', rawdata, flags=re.I)
    rawdata = re.sub('</?(DOCUMENT|TEXT|HTML|HEAD|BODY|P|DIV|HR|TABLE|TR|TH|DL|DT|UL).*?>', '\n', rawdata, flags=re.I)
    rawdata = re.sub('</?(A|FONT|B|BR|TYPE|SEQUENCE|FILENAME|DESCRIPTION|DD|I|SUP|!--).*?>', ' ', rawdata, flags=re.I)
    rawdata = re.sub('</?(TD).*?>', '    ', rawdata, flags=re.I)
    rawdata = re.sub('&nbsp;', ' ', rawdata, flags=re.I)
    rawdata = re.sub('(\n)\s+', '\n', rawdata, flags=re.I)
    return rawdata
