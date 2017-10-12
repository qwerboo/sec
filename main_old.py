from openpyxl import load_workbook
from search import Scrape
from db import Mydb
from tools import obj_to_dict
import pymysql
import time
import queue
import threading
import traceback
import logging

class Productor(threading.Thread):
    def __init__(self, tName, q):
        self.q = q
        threading.Thread.__init__(self, name=tName)

    def run(self):
        print("%s start"%threading.current_thread().name)
        wb = load_workbook('CIK.xlsx')
        sheet = wb.get_sheet_by_name('Sheet1')
        for v in sheet.values:
            self.q.put(v[0])
            print('queue`s size:%s'%self.q.qsize())
        print("%s end"%threading.current_thread().name)

class Consumer(threading.Thread):
    def __init__(self, tName, q):
        self.q = q
        threading.Thread.__init__(self, name=tName)
        self.db = Mydb()
        self.scrape = Scrape()

    def run(self):
        print("%s start"%threading.current_thread().name)
        results = self.db.get('sec.tb_file', 'url')
        fileSet = set(record[0] for record in results)
        self.scrape.create_session()
        while True:
            try:
                cik = self.q.get(True, 30)
            except queue.Empty:
                print("%s end"%threading.current_thread().name)
                break
            ctime = time.strftime('%Y-%m-%d %H:%M:%S')
            try:
                int(cik)
            except ValueError as e:
                traceback.print_exc()
                continue
            print('%s:%s'%(threading.current_thread().name,cik))
            try:
                r = self.db.get_one('sec.tb_company', 'id, is_ok', {'cik':cik})
            except Exception as e:
                if self.db.conn:
                    self.db.conn.close()
                self.db.conn = None
                traceback.print_exc()
                continue
            if r and r[1] == 1:
                continue
            elif r:
                companyid = r[0]
            try:
                company, urls = self.scrape.document_list(cik)
            except Exception as e:
                traceback.print_exc()
                continue
            company.ctime_ = ctime
            try:
                if not companyid:
                    companyid = self.db.insert('sec.tb_company', obj_to_dict(company))
            except Exception as e:
                if self.db.conn:
                    self.db.conn.close()
                self.db.conn = None
                traceback.print_exc()
                continue
            for url in urls:
                print('%s:file list,%s'%(threading.current_thread().name,url))
                try:
                    doc, files = self.scrape.file_list(url)
                except Exception as e:
                    traceback.print_exc()
                    continue
                doc.company_id_ = companyid
                try:
                    r = self.db.get_one('sec.tb_document', 'id', {'url':url})
                except Exception as e:
                    if self.db.conn:
                        self.db.conn.close()
                    self.db.conn = None
                    traceback.print_exc()
                    continue
                if not r:
                    try:
                        documentid = self.db.insert('sec.tb_document', obj_to_dict(doc))
                    except Exception as e:
                        if self.db.conn:
                            self.db.conn.close()
                        self.db.conn = None
                        traceback.print_exc()
                        continue
                else:
                    documentid = r[0]
                for record in files:
                    if record[2] in fileSet:
                        print("已存在：%s"%record[2])
                        continue
                    print('%s:file,%s'%(threading.current_thread().name, record[2]))
                    try:
                        f = self.scrape.extract_rawdata(record)
                    except Exception as e:
                        self.scrape.create_session()
                        traceback.print_exc()
                        continue
                    f.company_id_ = companyid
                    f.doc_id_ = documentid
                    try:
                        self.db.insert('sec.tb_file', obj_to_dict(f))
                    except Exception as e:
                        if self.db.conn:
                            self.db.conn.close()
                        self.db.conn = None
                        traceback.print_exc()
                        continue
                    self.db.conn.commit()
                    fileSet.add(f.url_)
            try:
                self.db.update('sec.tb_company', {'is_ok':1}, companyid)
            except Exception as e:
                if self.db.conn:
                    self.db.conn.close()
                self.db.conn = None
                traceback.print_exc()
                continue
            self.db.conn.commit()
        self.db.conn.close()

if __name__ == '__main__':
    q = queue.Queue(100)
    p = Productor('t_productor', q)
    c1 = Consumer('t_consumer1', q)
    c2 = Consumer('t_consumer2', q)
    c3 = Consumer('t_consumer3', q)
    c4 = Consumer('t_consumer4', q)
    c5 = Consumer('t_consumer5', q)
    p.start()
    c1.start()
    c2.start()
    c3.start()
    c4.start()
    c5.start()
    p.join()
    c1.join()
    c2.join()
    c3.join()
    c4.join()
    c5.join()
