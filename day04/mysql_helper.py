# -*- coding: utf-8 -*-

__author__ = "wuyou"
__date__ = "2018/6/7 9:35"

'''
采用sqlalchemy 定义实体类, 进行ORM操作
'''
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey


'''
基本过程：
1. 获取实体数据库连接
2. 创建类，继承基类，用基本类型描述数据库结构
3. 基类调用类结构，根据描述在引擎上创建数据表
'''

# 数据库连接
mysql_conn_str = "mysql+pymysql://root:123456@127.0.0.1:3306/books"

# 引擎
engine = create_engine(mysql_conn_str)

# 基类
Base = declarative_base()


# 元素
class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    book_title = Column(String(300))
    image_url = Column(String(300))
    book_url = Column(String(300))
    book_rate = Column(String(20))
    book_price = Column(String(20))

'''
初始化DB, 进行模型 --> 数据库 同步
'''

# 创建表
Base.metadata.create_all(engine)


def create_session():
    #  Session的主要目的是建立与数据库的会话，它维护你加载和关联的所有数据库对象。
    #  它是数据库查询（Query）的一个入口
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


'''
add record to session.
objs --> (1) [obj1, obj2]  (2) obj
'''


def add_records(session, objs):
    if isinstance(objs, list):
        session.add_all(objs)
    else:
        session.add(objs)
    session.commit()


'''
查询数据模型中的db数据
'''
def query_record(session, Cls):
    return session.query(Cls).all()


# if __name__ == '__main__':
    # session = create_session()
    # records = query_record(session, Book)
    # for rec in records:
    #     print(rec.book_title)










