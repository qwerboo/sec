from db import Mydb
import re
import time
import sys

keyword_interest = 'Interest rate'
keyword_forex = '|'.join(['currency', 'foreign exchange', 'exchange rate'])
keyword_b = '|'.join(['forward', 'forwards', 'future', 'futures', 'option', 'options', 'swap', 'swaps', 'spot', 'spots', 'collar', 'collars', 'cap', 'caps', 'ceiling', 'ceilings', 'floor', 'floors', 'lock', 'locks', 'derivative', 'derivatives', 'hedge', 'hedges', 'hedging', 'hedged'])
keyword_c = '|'.join(['contract', 'contracts', 'position', 'positions', 'instrument', 'instruments', 'agreement', 'agreements', 'obligation', 'obligations', 'transaction', 'transactions', 'strategy', 'strategies'])

keyword_not = ['in the future', 'not', 'insignificant']
# 'a[\s\W]*(\w+[\s\W]*){0,2}[\s\W]*b'
# 'a[^<>\w]*(\w+[^<>\w]*){0,2}[^<>\w]*b'
reg = '((%s)[^<>]*?(%s)[^<>]*?(%s))'
# reg = '(%s)[ ,.;:\'\(\)]{26}(%s)[ ,.;:\'\(\)]{26}(%s)'
# reg_model = '((%s)[^<>\w]*(\w+[^<>\w]*){0,25}[^<>\w]*(%s)[^<>\w]*(\w+[^<>\w]*){0,25}[^<>\w]*(%s))'
# reg = '((%s)[^<>]*(\w+[^<>]*){0,25}[^<>]*(%s)[^<>]*(\w+[^<>]*){0,25}[^<>\w]*(%s))'

reg_interest_0 = reg%(keyword_interest, keyword_b, keyword_c)
reg_interest_1 = reg%(keyword_interest, keyword_c, keyword_b)
reg_interest_2 = reg%(keyword_c, keyword_b, keyword_interest)
reg_interest_3 = reg%(keyword_c, keyword_interest, keyword_b)
reg_interest_4 = reg%(keyword_b, keyword_c, keyword_interest)
reg_interest_5 = reg%(keyword_b, keyword_interest, keyword_c)
reg_interest = [reg_interest_0,reg_interest_1,reg_interest_2,reg_interest_3,reg_interest_4,reg_interest_5]

reg_forex_0 = reg%(keyword_forex, keyword_b, keyword_c)
reg_forex_1 = reg%(keyword_forex, keyword_c, keyword_b)
reg_forex_2 = reg%(keyword_c, keyword_b, keyword_forex)
reg_forex_3 = reg%(keyword_c, keyword_forex, keyword_b)
reg_forex_4 = reg%(keyword_b, keyword_c, keyword_forex)
reg_forex_5 = reg%(keyword_b, keyword_forex, keyword_c)
reg_forex = [reg_forex_0, reg_forex_1, reg_forex_2, reg_forex_3, reg_forex_4, reg_forex_5]

def main(env):
    db = Mydb(env)
    pageNum = 0
    # reg_interest = []
    # reg_forex = []
    # for inter in keyword_interest:
    #     reg = reg_model%(inter, '|'.join(keyword_b), '|'.join(keyword_c))
    #     reg_interest.append(reg)
    # for inter in keyword_interest:
    #     reg = reg_model%(inter, '|'.join(keyword_c), '|'.join(keyword_b))
    #     reg_interest.append(reg)
    # for inter in keyword_b:
    #     reg = reg_model%(inter, '|'.join(keyword_interest), '|'.join(keyword_c))
    #     reg_interest.append(reg)
    # for inter in keyword_b:
    #     reg = reg_model%(inter, '|'.join(keyword_c), '|'.join(keyword_interest))
    #     reg_interest.append(reg)
    # for inter in keyword_c:
    #     reg = reg_model%(inter, '|'.join(keyword_interest), '|'.join(keyword_b))
    #     reg_interest.append(reg)
    # for inter in keyword_c:
    #     reg = reg_model%(inter, '|'.join(keyword_b), '|'.join(keyword_interest))
    #     reg_interest.append(reg)
    #
    # for inter in keyword_forex:
    #     reg = reg_model%(inter, '|'.join(keyword_b), '|'.join(keyword_c))
    #     reg_forex.append(reg)
    # for inter in keyword_forex:
    #     reg = reg_model%(inter, '|'.join(keyword_c), '|'.join(keyword_b))
    #     reg_forex.append(reg)
    # for inter in keyword_b:
    #     reg = reg_model%(inter, '|'.join(keyword_forex), '|'.join(keyword_c))
    #     reg_forex.append(reg)
    # for inter in keyword_b:
    #     reg = reg_model%(inter, '|'.join(keyword_c), '|'.join(keyword_forex))
    #     reg_forex.append(reg)
    # for inter in keyword_c:
    #     reg = reg_model%(inter, '|'.join(keyword_forex), '|'.join(keyword_b))
    #     reg_forex.append(reg)
    # for inter in keyword_c:
    #     reg = reg_model%(inter, '|'.join(keyword_b), '|'.join(keyword_forex))
    #     reg_forex.append(reg)
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
            for reg in reg_interest:
                print(reg)
                for m in re.findall(reg, rawdata):
                    # print('%s:hint!!'%(fileId))
                    flag = True
                    for kn in keyword_not:
                        if m[0].find(kn) != -1:
                            flag = False
                            break
                    if flag:
                        hintInterest = hintInterest+1
                        db.insert('sec.t_hints_files', {'file_id':fileId, 'hint_type':1, 'paragraph': m[0]})
            for reg in reg_forex:
                for m in re.findall(reg, rawdata):
                    # print('%s:hint!!'%(fileId))
                    flag = True
                    for kn in keyword_not:
                        if m[0].find(kn) != -1:
                            flag = False
                            break
                    if flag:
                        hintForex = hintForex+1
                        db.insert('sec.t_hints_files', {'file_id':fileId, 'hint_type':2, 'paragraph': m[0]})
            db.insert('sec.t_hints', {'company_id':companyId, 'doc_id':docId, 'file_id':fileId, 'hint_interest':hintInterest, 'hint_forex':hintForex, 'ctime':ctime})
            print(time.strftime('%Y-%m-%d %H:%M:%S'), fileId, hintInterest, hintForex)
            db.conn.commit()

if __name__ == '__main__':
    main(sys.argv[1])
