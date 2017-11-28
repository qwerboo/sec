from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pymysql

es = Elasticsearch()

def get_conn():
    conn = pymysql.connect(host='rm-2ze0ek7c57w65y4t6o.mysql.rds.aliyuncs.com',
                        user='ip_infos_root',
                        passwd='zcb!1511',
                        charset="utf8mb4"
                        )
    cur = conn.cursor()
    return conn, cur


def main_syn_rawdata():
    '同步原始文书'
    sql = "SELECT caseid, rawdata from ip_infos.t_case_rawdata where caseid > %s order by caseid limit 10"
    conn, cur = get_conn()
    pageNum = 352664
    while True:
        if cur.execute(sql, pageNum):
            actions = []
            for record in cur.fetchall():
                caseid = record[0]
                rawdata = record[1]
                pageNum = caseid
                doc = {
                    '_index': 'zcb_rawdata',
                    '_type': 'rawdata',
                    '_id': caseid,
                    '_source': {
                        'rawdata': rawdata,
                        'timestamp': datetime.now()}
                }
                actions.append(doc)
            print(pageNum)
            res = helpers.bulk(es, actions)
            print(res)
            # break
        else:
            break

if __name__ == '__main__':
    main_syn_rawdata()
