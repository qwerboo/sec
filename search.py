import requests
import re
from bs4 import BeautifulSoup
from entity import Company, Document, File
from db import Mydb
from tools import obj_to_dict
import pymysql
import sys


class Scrape(object):
    def __init__(self):
        self.search_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-k&dateb=&owner=exclude&count=100"
        self.headers = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Accept":"*/*",
            "Accept-Language":"en-GB,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
            "accept-encoding":"gzip, deflate, br",
            "charset":"UTF-8"
        }
        self.session = requests.Session()
        self.session.headers = self.headers

    def document_list(self, cik):
        url = self.search_url.format(cik=cik)
        listPage = self.session.get(url)
        bs = BeautifulSoup(listPage.content, 'html.parser')
        company = Company()
        companyName = bs.find('span', {'class', 'companyName'}).text
        company.name_ = re.search('(.*)CIK', companyName).group(1)
        company.cik_ = re.search('CIK#: (\d*)', companyName).group(1)
        identInfo = bs.find('p', {'class', 'identInfo'}).text
        match = re.search('SIC:(.*)State location: (.*)\| State of Inc.:(.*)\| Fiscal Year End: (\d*)', identInfo)
        if not match:
            match = re.search('SIC:(.*)State location: (.*) ()\| Fiscal Year End: (\d*)', identInfo)
        if match:
            company.sic_ = match.group(1).strip()
            company.location_ = match.group(2).strip()
            company.state_of_inc_ = match.group(3).strip()
            company.fiscal_year_end_ = match.group(4).strip()
        address = bs.findAll('div', {'class', 'mailer'})
        for addr in address[0].findAll('span', {'class', 'mailerAddress'}):
            if not company.maddr_street_:
                company.maddr_street_ = addr.text
            elif not company.maddr_city_:
                match = re.search('(.*) ([\d-]+)', addr.text)
                if not match and addr.text.strip().endswith('STREET'):
                    company.maddr_street_ = company.maddr_street_ + ' ' + addr.text.strip()
                    continue
                elif not match:
                    continue
                company.maddr_city_ = match.group(1)
                # company.maddr_state_ = match.group(2)
                company.maddr_zip_ = match.group(2)
        for addr in address[1].findAll('span', {'class', 'mailerAddress'}):
            if not company.baddr_street_:
                company.baddr_street_ = addr.text
            elif not company.baddr_city_:
                match = re.search('(.*) ([\d-]+)', addr.text)
                if not match and addr.text.strip().endswith('STREET'):
                    company.maddr_street_ = company.maddr_street_ + ' ' + addr.text.strip()
                    continue
                elif not match:
                    continue
                company.baddr_city_ = match.group(1)
                # company.baddr_state_ = match.group(2)
                company.baddr_zip_ = match.group(2)
            elif not company.baddr_phone_:
                company.baddr_phone_ = addr.text
        urls = []
        table = bs.find('table', {'class', 'tableFile2'})
        if table:
            for tr in table.findAll('tr'):
                a = tr.find('a', {'id': 'documentsbutton'})
                if a:
                    td = tr.find('td')
                    if td.text.strip() != '10-K/A':
                        urls.append('https://www.sec.gov%s'%a.attrs['href'])
        # for doc in bs.findAll('a', {'id': 'documentsbutton'}):
        #     urls.append('https://www.sec.gov%s'%doc.attrs['href'])
        return company, urls

    def file_list(self, url):
        listPage = self.session.get(url)
        doc = Document()
        bs = BeautifulSoup(listPage.content, 'html.parser')
        doc.url_ = url
        doc.acc_no_ = re.search('.*/(.*)-index.htm', url).group(1)
        infos = bs.findAll('div',{'class','info'})
        doc.filing_date_ = infos[0].text
        doc.accepted_ = infos[1].text
        doc.documents_ = infos[2].text
        doc.period_of_report_ = infos[3].text
        companyName = bs.find('span', {'class', 'companyName'}).text
        doc.company_name_ = re.search('(.*)\(', companyName).group(1)
        identInfo = bs.find('p', {'class', 'identInfo'}).text
        match = re.search('IRS No.: (.*) \| State of Incorp.: (.*) \| Fiscal Year End: (.*)Type: (.*) \| Act: (.*) \| File No.: (.*) \| Film No.: (.*)SIC: (.*)', identInfo)
        if not match:
            match = re.search('IRS No.: (.*) \| State of Incorp.: (.*)()Type: (.*) \| Act: (.*) \| File No.: (.*) \| Film No.: (.*)SIC: (.*)', identInfo)
            if not match:
                match = re.search('IRS No.: (.*)() \| Fiscal Year End: (.*)Type: (.*) \| Act: (.*) \| File No.: (.*) \| Film No.: (.*)SIC: (.*)', identInfo)
        if match:
            doc.state_of_inc_ = match.group(2)
            doc.fiscal_year_end_ = match.group(3)
            doc.type_ = match.group(4)
            doc.sic_ = match.group(8)
        address = bs.findAll('div', {'class', 'mailer'})
        for addr in address[0].findAll('span', {'class', 'mailerAddress'}):
            if not doc.maddr_street_:
                doc.maddr_street_ = addr.text
            elif not doc.maddr_city_:
                print(addr.text)
                match = re.search('(.*) ([\d-]+)', addr.text)
                if not match and addr.text.strip().endswith('STREET'):
                    doc.maddr_street_ = doc.maddr_street_ + ' ' + addr.text.strip()
                    continue
                elif not match:
                    continue
                doc.maddr_city_ = match.group(1)
                # doc.maddr_state_ = match.group(2)
                doc.maddr_zip_ = match.group(2)
        for addr in address[1].findAll('span', {'class', 'mailerAddress'}):
            if not doc.baddr_street_:
                doc.baddr_street_ = addr.text
            elif not doc.baddr_city_:
                match = re.search('(.*) ([\d-]+)', addr.text)
                if not match and addr.text.strip().endswith('STREET'):
                    doc.maddr_street_ = doc.maddr_street_ + ' ' + addr.text.strip()
                    continue
                elif not match:
                    continue
                doc.baddr_city_ = match.group(1)
                # doc.baddr_state_ = match.group(2)
                doc.baddr_zip_ = match.group(2)
            elif not doc.baddr_phone_:
                doc.baddr_phone_ = addr.text
        table = bs.find('table',{'class','tableFile'})
        files = []
        completeFile = None
        for tr in table.findAll('tr'):
            a = tr.find('a')
            if a:
                url = a.attrs['href']
                tds = tr.findAll('td')
                if url.endswith('.htm'):
                    files.append((tds[0].text, tds[1].text,'https://www.sec.gov%s'%url, tds[3].text, tds[4].text))
                elif url.endswith('.txt'):
                    completeFile = (0, tds[1].text,'https://www.sec.gov%s'%url, tds[3].text, tds[4].text)
        if not files and completeFile:
            files.append(completeFile)
        return doc, files

    def extract_rawdata(self, record):
        f = File()
        f.seq_ = record[0]
        f.describtion_ = record[1]
        f.url_ = record[2]
        f.type_ = record[3]
        f.size_ = record[4]
        try:
            source = self.session.get(f.url_)
        except Exception as e:
            raise e
        if f.url_.endswith('.txt'):
            f.rawdata_ = source.content
        else:
            bs = BeautifulSoup(source.content, 'html.parser')
            paragraphs = bs.findAll('div')
            if not paragraphs:
                paragraphs = bs.findAll('p')
            rawdata = ''
            for para in paragraphs:
                text = para.text
                text = re.sub('[\t\r\n]+', '', text)
                if text:
                    if isinstance(text, int):
                        text = str(text)
                    rawdata += text + '\n'
            f.rawdata_ = rawdata
            f.msize = sys.getsizeof(f.rawdata_)/1000000
        return f

if __name__ == '__main__':
    scrape = Scrape()
    scrape.create_session()
    record = [1, '', '', '', 0]
    record[0] = 1
    record[1] = ''
    record[2] = 'https://www.sec.gov/Archives/edgar/data/356213/0000898430-96-001157.txt'
    record[3] = ''
    record[4] = 0
    scrape.extract_rawdata(record)
