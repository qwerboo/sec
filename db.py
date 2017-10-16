import pymysql

class Mydb(object):
    """ 数据库操作类 """
    def __init__(self, host='ec2-54-250-215-159.ap-northeast-1.compute.amazonaws.com', user='root', passwd='AI2017aws'):
        self.conn = pymysql.connect(host=host,
                            user=user,
                            passwd=passwd,
                            charset="utf8mb4",
                            max_allowed_packet=1024000000)
        self.cur = self.conn.cursor()

    def get(self, table, fields, option=None, orderby=None, limit=None):
        sql = "SELECT {fields} from {table} where 1=1 {opt}"
        opt = ''
        if option:
            # for k,v in option.items():
            #     opt += " and {}='{}'".format(k, v)
            opt += " and {}".format(option)
        sql = sql.format(fields=fields, table=table, opt=opt)
        if orderby:
            sql = "%s order by %s"%(sql, orderby)
        if limit:
            sql = "%s limit %d"%(sql, limit)
        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_one(self, table, fields, option):
        sql = "SELECT {fields} from {table} where 1=1 {opt}"
        opt = ""
        if option:
            for k,v in option.items():
                opt += " and {}='{}'".format(k, v)
        sql = sql.format(fields=fields, table=table, opt=opt)
        if self.cur.execute(sql):
            return self.cur.fetchone()
        else:
            return None

    def update(self, table, data, id):
        sql = "UPDATE {table} set {params} where id = {id}"
        params = ""
        for k,v in data.items():
            # if isinstance(v, str):
            #     v = v.replace('%', '\%')
            params += "{}='{}',".format(k,v)
        params = params[:-1]
        sql = sql.format(table=table, params=params, id=id)
        self.cur.execute(sql)

    def insert(self, table, data):
        fields = ""
        params = []
        fields = ""
        values = ""
        for k,v in data.items():
            fields += "%s,"%k
            values += "%s,"
            params.append(v)
        fields = fields[:len(fields)-1]
        table = "{}({})".format(table, fields)
        values = values[:len(values)-1]
        values = "({})".format(values)
        params = tuple(params)
        sql = "INSERT into {table} values {values}".format(table=table, values=values)
        try:
            self.cur.execute(sql, params)
        except pymysql.err.OperationalError as e:
            raise e
        return self.cur.lastrowid


if __name__ == "__main__":
    db = Mydb("127.0.0.1", "root", "root")
    db.update("linkin.t_source", {"scraped":1, "linkin_url":"https://www.linkedin.com/in/robert-a-zuccaro-4467a25"}, 6)
