class Company(object):
    ''' 基本资料 '''
    def __init__(self):
        self.id_ = None
        self.cik_ = ''                  # CENTRAL INDEX KEY
        self.name_ = ''                 # 公司名
        self.sic_ = ''                  # STANDARD INDUSTRIAL CLASSIFICATION 标准产业分类
        self.location_ = ''             # State location
        self.state_of_inc_ = ''         # state of incorporation 注册状态
        self.fiscal_year_end_ = ''      # Fiscal Year End 会计年度
        self.baddr_street_ = ''         # 地址 街道，城市，州，邮编，电话
        self.baddr_city_ = ''
        self.baddr_state_ = ''
        self.baddr_zip_ = ''
        self.baddr_phone_ = ''
        self.maddr_street_ = ''         # 邮件地址 街道，城市，州，邮编
        self.maddr_city_ = ''
        self.maddr_state_ = ''
        self.maddr_zip_ = ''
        self.ctime_ = ''

    def __repr__(self):
        return '<cik % r>' % self.cik_ + '\n' \
                '<公司名字 % r>' % self.name_ + '\n' \
                '<产业分类 id % r>' % self.sic_ + '\n' \
                '<州 % r>' % self.location_ + '\n' \
                '<注册状态 % r>' % self.state_of_inc_ + '\n' \
                '<会计年度 % r>' % self.fiscal_year_end_ + '\n' \
                '<地址 %r\n%r\n%r\n%r\n%r>' % (self.baddr_street_,self.baddr_city_,self.baddr_state_,self.baddr_zip_,self.baddr_phone_) + '\n' \
                '<邮件地址 %r\n%r\n%r\n%r>' % (self.maddr_street_,self.maddr_city_,self.maddr_state_,self.maddr_zip_) + '\n'

class Document(object):
    ''' 归档 '''
    def __init__(self):
        self.id_ = None                 #
        self.acc_no_ = ''               # 编号
        self.url_ = ''
        self.company_id_ = None
        self.type_ = ''                 # 类型 10-k
        self.filing_date_ = ''          # 归档日期
        self.period_of_report_ = ''     # 报告日期
        self.accepted_ = ''             # 接受日期
        self.documents_ = None          # 文档数量
        self.company_name_ = ''
        self.sic_ = ''                  # STANDARD INDUSTRIAL CLASSIFICATION 标准产业分类
        self.state_of_inc_ = ''         # state of incorporation 注册状态
        self.fiscal_year_end_ = ''      # Fiscal Year End 会计年度
        self.baddr_street_ = ''         # 地址 街道，城市，州，邮编，电话
        self.baddr_city_ = ''
        self.baddr_state_ = ''
        self.baddr_zip_ = ''
        self.baddr_phone_ = ''
        self.maddr_street_ = ''         # 邮件地址 街道，城市，州，邮编
        self.maddr_city_ = ''
        self.maddr_state_ = ''
        self.maddr_zip_ = ''

    def __repr__(self):
        return '<编号 % r>' % self.acc_no_ + '\n' \
                '<企业ID % r>' % self.company_id_ + '\n' \
                '<类型 % r>' % self.type_ + '\n' \
                '<归档日期 % r>' % self.filing_date_ + '\n' \
                '<报告日期 % r>' % self.period_of_report_ + '\n' \
                '<接受日期 % r>' % self.accepted_ + '\n' \
                '<文档数量 % r>' % self.documents_ + '\n' \
                '<公司名 % r>' % self.company_name_ + '\n' \
                '<产业分类 % r>' % self.sic_ + '\n' \
                '<注册状态 % r>' % self.state_of_inc_ + '\n' \
                '<会计年度 % r>' % self.fiscal_year_end_ + '\n' \
                '<地址 %r\n%r\n%r\n%r\n%r>' % (self.baddr_street_,self.baddr_city_,self.baddr_state_,self.baddr_zip_,self.baddr_phone_) + '\n' \
                '<邮件地址 %r\n%r\n%r\n%r>' % (self.maddr_street_,self.maddr_city_,self.maddr_state_,self.maddr_zip_) + '\n'

class File(object):
    ''' 文件 '''
    def __init__(self):
        self.id_ = None             #
        self.company_id_ = None     # company id
        self.doc_id_ = None         # document id
        self.url_ = ''              # 编号
        self.seq_ = None            # 序号
        self.describtion_ = ''      # 描述
        self.type_ = ''             # 类型
        self.size_ = None           # 大小
        self.source_ = ''           # 源文件
        self.rawdata_ = ''          # 清理后的文本文档

    def __repr__(self):
        return '<编号 % r>' % self.acc_no_ + '\n' \
                '<归档ID % r>' % self.filing_id_ + '\n' \
                '<类型 % r>' % self.type_ + '\n' \
                '<文件大小 id % r>' % self.size_ + '\n' \
                '<描述 % r>' % self.desc_ + '\n' \
                '<序号 % r>' % self.seq_ + '\n'
