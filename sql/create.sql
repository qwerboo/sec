create table tb_company(
  id int not null auto_increment,
  cik varchar(20) comment'CENTRAL INDEX KEY',
  name varchar(200) comment'',
  sic varchar(200) comment'STANDARD INDUSTRIAL CLASSIFICATION 标准产业分类',
  location varchar(200) comment'State location',
  state_of_inc varchar(20) comment'state of incorporation 注册状态',
  fiscal_year_end varchar(50) comment'Fiscal Year End 会计年度',
  baddr_street varchar(200) comment'地址 街道，城市，州，邮编，电话',
  baddr_city varchar(100) comment'',
  baddr_state varchar(50) comment'',
  baddr_zip varchar(50) comment'',
  baddr_phone varchar(50) comment'',
  maddr_street varchar(200) comment'邮件地址 街道，城市，州，邮编',
  maddr_city varchar(100) comment'',
  maddr_state varchar(50) comment'',
  maddr_zip varchar(50) comment'',
  primary key(id)
)
COMMENT='公司'
COLLATE='utf8mb4_general_ci'
ENGINE='InnoDB'
;

create table tb_document(
  id int not null auto_increment,
  acc_no varchar(50) comment'编号',
  company_id int comment'',
  type varchar(20) comment'文档类型',
  filing_date varchar(50) comment'归档日期',
  period_of_report varchar(50) comment'报告日期',
  accepted varchar(50) comment'接受日期',
  documents int comment'文档数量',
  company_name varchar(200) comment'公司名称',
  sic varchar(200) comment'STANDARD INDUSTRIAL CLASSIFICATION 标准产业分类',
  state_of_inc varchar(20) comment'state of incorporation 注册状态',
  fiscal_year_end varchar(50) comment'Fiscal Year End 会计年度',
  baddr_street varchar(200) comment'地址 街道，城市，州，邮编，电话',
  baddr_city varchar(100) comment'',
  baddr_state varchar(50) comment'',
  baddr_zip varchar(50) comment'',
  baddr_phone varchar(50) comment'',
  maddr_street varchar(200) comment'邮件地址 街道，城市，州，邮编',
  maddr_city varchar(100) comment'',
  maddr_state varchar(50) comment'',
  maddr_zip varchar(50) comment'',
  primary key(id)
)
COMMENT='文档'
COLLATE='utf8mb4_general_ci'
ENGINE='InnoDB'
;

create table tb_file(
  id int not null auto_increment,
  doc_id int comment'document id',
  url varchar(200) comment'',
  seq int comment'序号',
  describtion varchar(200) comment'描述',
  type varchar(20) comment'类型',
  size int comment'大小',
  source text comment'源文件',
  rawdata text comment'',
  primary key(id)
)
COMMENT='文件'
COLLATE='utf8mb4_general_ci'
ENGINE='InnoDB'
;

create table tmp_cik(
  id int not null auto_increment,
  cik varchar(20),
  primary key(id)
)
COMMENT='文件'
COLLATE='utf8mb4_general_ci'
ENGINE='InnoDB'
;
