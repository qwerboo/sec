from db import Mydb
import re
import time

keyword_interest = '|'.join(['Interest rate'])
keyword_forex = '|'.join(['currency', 'foreign exchange', 'exchange rate'])
keyword_b = '|'.join(['forward', 'forwards', 'future', 'futures', 'option', 'options', 'swap', 'swaps', 'spot', 'spots', 'collar', 'collars', 'cap', 'caps', 'ceiling', 'ceilings', 'floor', 'floors', 'lock', 'locks', 'derivative', 'derivatives', 'hedge', 'hedges', 'hedging', 'hedged'])
keyword_c = '|'.join(['contract', 'contracts', 'position', 'positions', 'instrument', 'instruments', 'agreement', 'agreements', 'obligation', 'obligations', 'transaction', 'transactions', 'strategy', 'strategies'])

keyword_not = ['in the future', 'not', 'insignificant']

reg = '(%s)[ ,.;:\'\(\)]{26}(%s)[ ,.;:\'\(\)]{26}(%s)'
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

def main():
    db = Mydb()
    pageNum = 0
    while True:
        files = db.get('sec.tb_file', 'id, company_id, doc_id, rawdata', option="id > %d"%pageNum, orderby='id', limit=1)
        for f in files:
            fileId = f[0]
            print(time.strftime('%Y-%m-%d %H:%M:%S'),fileId)
            pageNum = fileId
            companyId = f[1]
            docId = f[2]
            rawdata = f[3]
            paragraphs = rawdata.split('\n')
            hintInterest = 0
            hintForex = 0
            ctime = time.strftime('%Y-%m-%d %H:%M:%S')
            for para in paragraphs:
                for reg in reg_interest:
                    if para.strip():
                        match = re.search(reg, para)
                        if match:
                            flag = True
                            for kn in keyword_not:
                                if match.group().find(kn) != -1:
                                    flag = False
                                    break
                            if flag:
                                hintInterest = hintInterest+1
                                db.insert('sec.t_hints_files', {'file_id':fileId, 'hint_type':1, 'paragraph': para})
                for reg in reg_forex:
                    if para.strip():
                        match = re.search(reg, para)
                        if match:
                            flag = True
                            for kn in keyword_not:
                                if match.group().find(kn) != -1:
                                    flag = False
                                    break
                            if flag:
                                hintForex = hintForex+1
                                db.insert('sec.t_hints_files', {'file_id':fileId, 'hint_type':2, 'paragraph': para})
            db.insert('sec.t_hints', {'company_id':companyId, 'doc_id':docId, 'file_id':fileId, 'hint_interest':hintInterest, 'hint_forex':hintForex, 'ctime':ctime})
            print(time.strftime('%Y-%m-%d %H:%M:%S'), fileId, hintInterest, hintForex)
            db.conn.commit()

if __name__ == '__main__':
    main()
