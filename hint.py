from db import Mydb
import re
import time
import sys

keyword_interest = ''
keyword_forex = []
keyword_b = ['forward', 'forwards', 'future', 'futures', 'option', 'options', 'swap', 'swaps', 'spot', 'spots', 'collar', 'collars', 'cap', 'caps', 'ceiling', 'ceilings', 'floor', 'floors', 'lock', 'locks', 'derivative', 'derivatives', 'hedge', 'hedges', 'hedging', 'hedged']
keyword_c = ['contract', 'contracts', 'position', 'positions', 'instrument', 'instruments', 'agreement', 'agreements', 'obligation', 'obligations', 'transaction', 'transactions', 'strategy', 'strategies']

keyword_not = ['in the future', 'not', 'insignificant']

def main(env):
    db = Mydb(env)
    pageNum = 0
    while True:
        files = db.get('sec.tb_file', 'id, company_id, doc_id, source', option="id > %d"%pageNum, orderby='id', limit=1)
        if len(files) == 0:
            break
        for f in files:
            fileId = f[0]
            # print(time.strftime('%Y-%m-%d %H:%M:%S'),fileId)
            pageNum = fileId
            companyId = f[1]
            docId = f[2]
            rawdata = f[3]
            hintInterest = 0
            hintForex = 0
            ctime = time.strftime('%Y-%m-%d %H:%M:%S')
            index1 = 0
            for keyword in ['Interest rate', 'currency', 'foreign exchange', 'exchange rate']:
                while True:
                    index1 = rawdata.find(keyword, index1)
                    if index1 >= 0:
                        flag_b, flag_c = get_pos(rawdata, index1, keyword_b, keyword_c)
                        if not flag_b or not flag_c:
                            index, flag_c, flag_b = get_pos(rawdata, index1, keyword_c, keyword_b)
                        if flag_b and flag_c:
                            para = rawdata[min([index1, flag_b, flag_c]):max([index1, flag_b, flag_c])]
                            if keyword == 'Interest rate':
                                hintInterest += 1
                                db.insert('sec.t_hints_files', {'file_id':fileId, 'hint_type':1, 'paragraph': para})
                            else:
                                hintForex += 1
                                db.insert('sec.t_hints_files', {'file_id':fileId, 'hint_type':2, 'paragraph': para})
                    if index1 == -1:
                        break
                    index1 = index1 + len(keyword_interest)
            db.insert('sec.t_hints', {'company_id':companyId, 'doc_id':docId, 'file_id':fileId, 'hint_interest':hintInterest, 'hint_forex':hintForex, 'ctime':ctime})
            print(time.strftime('%Y-%m-%d %H:%M:%S'), fileId, hintInterest, hintForex)
            db.conn.commit()


def get_pos(rawdata, index1, keyword, keyword_b, keyword_c):
    flag_b = None
    flag_b_key = ''
    flag_c = None
    flag_c_key = ''
    for b in keyword_b:
        index2 = rawdata.find(b, index1+len(keyword))
        if index2 == -1:
            continue
        line = rawdata[index1+len(keyword):index2]
        if line.find('<')>=0 or line.find('>')>=0:
            continue
        if len(re.findall('\w+\W*', line)) > 25:
            continue
        if flag_b == None or index2 < flag_b:
            flag_b = index2 + len(b)
            flag_b_key = b
    if flag_b:
        for c in keyword_c:
            index3 = rawdata.find(c, index1+len(keyword))
            if index3 == -1:
                continue
            line = rawdata[flag_b:index3]
            if not line:
                line = rawdata[index3+len(c):flag_b-len(flag_b_key)]
            if line.find('<')>=0 or line.find('>')>=0:
                continue
            if len(re.findall('\w+\W*', line)) > 25:
                continue
            if flag_c == None or index3 < flag_c:
                flag_c = index3 + len(c)
                flag_c_key = c
            # hint!!
        if not flag_c:
            for c in keyword_c:
                index3 = rawdata.rfind(c, 0, index1)
                if index3 == -1:
                    continue
                line = rawdata[index3+len(c):index1]
                if line.find('<')>=0 or line.find('>')>=0:
                    continue
                if len(re.findall('\w+\W*', line)) > 25:
                    continue
                if flag_c == None or index3 < flag_c:
                    flag_c = index3 - len(c)
                    flag_c_key = c
                    index1 = index1 + len(keyword)
    else:
        for b in keyword_b:
            index2 = rawdata.rfind(b, 0, index1)
            if index2 == -1:
                continue
            line = rawdata[index2+len(b):index1]
            if line.find('<')>=0 or line.find('>')>=0:
                continue
            if len(re.findall('\w+\W*', line)) > 25:
                continue
            if flag_b == None or index2 < flag_b:
                flag_b = index2 - len(b)
                flag_b_key = b
                index1 = index1 + len(keyword)
        if flag_b:
            for c in keyword_c:
                index3 = rawdata.rfind(c, 0, index1 - len(keyword))
                if index3 == -1:
                    continue
                line = rawdata[flag_b+len(flag_b_key):index3]
                if not line:
                    line = rawdata[index3+len(c):flag_b]
                if line.find('<')>=0 or line.find('>')>=0:
                    continue
                if len(re.findall('\w+\W*', line)) > 25:
                    continue
                if flag_c == None or index3 < flag_c:
                    flag_c = index3 - len(c)
                    flag_c_key = c
            if not flag_c:
                for c in keyword_c:
                    index3 = rawdata.find(c, index1)
                    if index3 == -1:
                        continue
                    line = rawdata[index1:index3]
                    if len(re.findall('\w+\W*', line)) > 25:
                        continue
                    if flag_c == None or index3 < flag_c:
                        flag_c = index3 + len(c)
                        flag_c_key = c
    return index1, flag_b, flag_c

if __name__ == '__main__':
    main(sys.argv[1])
