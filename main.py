"""."""
from search import Scrape
import pymysql
import time
import traceback
import logging
from logging_config import setup_logging
from openpyxl import load_workbook
# from hint import get_hint
from entity import File
from clean import clean_file
from elasticsearch import Elasticsearch
from datetime import datetime
import requests


def get_conn():
    """."""
    conn = pymysql.connect(host='127.0.0.1',
                           user='root',
                           passwd='AI2017aws',
                           charset="utf8mb4"
                           )
    cur = conn.cursor()
    return conn, cur


def tmp_main():
    """."""
    setup_logging()
    logger = logging.getLogger(__name__)
    cik = int('0000000020')
    scrape = Scrape()
    company, urls = scrape.document_list(cik)
    for url in urls:
        doc, files = scrape.file_list(url)
        logger.info('fiscal_year_end_%s' % doc.filing_date_)
        for record in files:
            f = scrape.extract_rawdata(record)
            logger.info('文件大小：%s，文件实际大小：%s' % (f.size_, f.msize))
            hintInterest, hintForex = get_hint(f.source_.decode('utf-8'))
            logger.info('hintInterest:%s, hintForex:%s' %
                        (hintInterest, hintForex))


def main():
    """保存公司基本信息."""
    setup_logging()
    logger = logging.getLogger(__name__)
    conn, cur = get_conn()
    sql = "SELECT url from sec.tb_file"
    sqlOk = "SELECT id, is_ok from sec.tb_company where cik = %s"
    sqlInsertCompany = """INSERT into sec.tb_company(cik, name, sic, location, state_of_inc,
                        fiscal_year_end, baddr_state, baddr_city,
                        baddr_street, baddr_zip, baddr_phone,
                        maddr_street, maddr_city, maddr_state,
                        maddr_zip, ctime)
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s)"""
    sqkUpdateCompany = "UPDATE sec.tb_company set is_ok = 1 where id = %s"
    sqlDoc = "SELECT id from sec.tb_document where url = %s"
    sqlInsetDoc = """INSERT into sec.tb_document(acc_no, url, company_id, type, filing_date,
                    period_of_report, accepted, documents, company_name,
                    sic, state_of_inc, fiscal_year_end, baddr_street,
                    baddr_city, baddr_state, baddr_zip, baddr_phone,
                    maddr_street, maddr_city, maddr_state, maddr_zip)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s)"""
    sqlInsertFile = "INSERT into sec.tb_file(company_id, doc_id, url, seq, describtion, type, \
                    size) values(%s,%s,%s,%s,%s,%s,%s)"
    fileSet = set()
    if cur.execute(sql):
        fileSet = set(record[0] for record in cur.fetchall())
    scrape = Scrape()
    wb = load_workbook('CIK.xlsx')
    sheet = wb.get_sheet_by_name('Sheet1')
    for v in sheet.values:
        ctime = time.strftime('%Y-%m-%d %H:%M:%S')
        cik = v[0]
        try:
            int(cik)
        except ValueError as e:
            continue
        logger.debug('cik:%s' % cik)
        companyid = None
        isOk = 0
        if cur.execute(sqlOk, cik):
            record = cur.fetchone()
            companyid = record[0]
            isOk = record[1]
        if not isOk:
            try:
                company, urls = scrape.document_list(cik)
            except Exception as e:
                if e.args[0] == 'No matching CIK':
                    logger.debug('No matching CIK:%s' % cik)
                    continue
                else:
                    raise e
        else:
            continue
        if not companyid:
            print(company)
            cur.execute(sqlInsertCompany, (
                company.cik_, company.name_, company.sic_,
                company.location_, company.state_of_inc_,
                company.fiscal_year_end_, company.baddr_state_,
                company.baddr_city_, company.baddr_street_, company.baddr_zip_,
                company.baddr_phone_, company.maddr_street_,
                company.maddr_city_, company.maddr_state_,
                company.maddr_zip_, ctime))
            companyid = cur.lastrowid
            conn.commit()
        logger.debug('公司ID:%s,cik:%s' % (companyid, cik))
        for url in urls:
            doc, files = scrape.file_list(url)
            doc.company_id_ = companyid
            if cur.execute(sqlDoc, url):
                docId = cur.fetchone()[0]
            else:
                cur.execute(sqlInsetDoc, (
                    doc.acc_no_, url, doc.company_id_, doc.type_,
                    doc.filing_date_,
                    doc.period_of_report_, doc.accepted_, doc.documents_,
                    doc.company_name_,
                    doc.sic_, doc.state_of_inc_, doc.fiscal_year_end_,
                    doc.baddr_street_,
                    doc.baddr_city_, doc.baddr_state_, doc.baddr_zip_,
                    doc.baddr_phone_,
                    doc.maddr_street_, doc.maddr_city_, doc.maddr_state_,
                    doc.maddr_zip_))
                docId = cur.lastrowid
                conn.commit()
            for record in files:
                if record[2] not in fileSet:
                    f = File()
                    f.seq_ = record[0]
                    f.describtion_ = record[1]
                    f.url_ = record[2]
                    f.type_ = record[3]
                    f.size_ = record[4]
                    f.company_id_ = companyid
                    f.doc_id_ = docId
                    cur.execute(sqlInsertFile, (
                        f.company_id_, f.doc_id_, f.url_, f.seq_,
                        f.describtion_, f.type_, f.size_))
                    conn.commit()
                    fileSet.add(f.url_)
        cur.execute(sqkUpdateCompany, companyid)
        conn.commit()


def main_es():
    """保存企业发布的文档."""
    session = requests.Session()
    conn, cur = get_conn()
    sql = """SELECT id, company_id, doc_id, url from sec.tb_file
        where id>%s order by id limit 100"""
    pageNum = 86511
    es = Elasticsearch()
    while True:
        if cur.execute(sql, pageNum):
            for record in cur.fetchall():
                fileId = record[0]
                pageNum = fileId
                companyId = record[1]
                docId = record[2]
                url = record[3]
                content = session.get(url).text
                # source = session.get(url).text
                # rawdata = clean_file(source)
                doc = {
                    'company_id': companyId,
                    'doc_id': docId,
                    'url': url,
                    'content': content,
                    # 'source': source,
                    # 'rawdata': rawdata,
                    'timestamp': datetime.now()
                }
                res = es.index(index="sec_file", doc_type='file',
                               id=fileId, body=doc)
                print(fileId, res['result'])
        else:
            break


if __name__ == '__main__':
    main_es()
