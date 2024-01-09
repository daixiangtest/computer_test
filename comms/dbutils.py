import time

import pymysql
from comms.yaml_utils import get_ini_data
from comms.constants import CFI

"""
数据库封装
"""


class DBUtils:
    count = -1

    # 封装连接对象和游标对象
    def __init__(self):
        try:
            self.conn = pymysql.connect(host=get_ini_data(CFI, 'mysql', 'host'),
                                        port=int(get_ini_data(CFI, 'mysql', 'port')),
                                        user=get_ini_data(CFI, 'mysql', 'user'),
                                        passwd=get_ini_data(CFI, 'mysql', 'passwd'),
                                        db=get_ini_data(CFI, 'mysql', 'db'))
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("数据库工具类连接出现异常,请检查DBUtils类中的__init__方法!")
            raise  # e代表异常的原因

    # 封装关闭游标对象和连接对象
    def close(self):
        self.cursor.close()
        self.conn.close()

    # 封装增删改
    # 如果execute()括号内只传一个参数,我们运行 execute(sql)
    # 如果execute()括号内传两个参数,如果是元组占位符参数我们运行 execute(sql,params),如果是列表则执行executemany(sql,params)
    def cud(self, sql, params=None):
        try:
            if params is None:  # 判断传了几个参数,如果只传了一个参数,那么就执行execute(sql)
                self.count = self.cursor.execute(sql)
            if isinstance(params, tuple):  # 判断传入的参数是不是元组,是元组类型执行execute(sql,params)
                self.count = self.cursor.execute(sql, params)
            if isinstance(params, list):  # 判断传入的参数是不是列表,是列表类型执行executemany(sql,params)
                self.count = self.cursor.executemany(sql, params)
            self.conn.commit()
            return self.count  # 返回sql影响的条目数
        except Exception as e:
            print("增删改失败!", e)
        # finally:
        #     self.cursor.close()
        #     self.conn.close()

    # 封装查询结果集有多少条数据: 条目数
    # 如果execute()括号内只传一个参数,我们运行 execute(sql)
    # 如果execute()括号内传两个参数,我们运行 execute(sql,params)
    def find_count(self, sql, params=None):
        try:
            if params is None:
                self.count = self.cursor.execute(sql)
            elif params is not None:
                self.count = self.cursor.execute(sql, params)
            return self.count
        except Exception as e:
            print("查询数据库条目数失败!", e)
        # finally:
        #     self.cursor.close()
        #     self.conn.close()

    # 封装查询一条数据: 要求返回具体的数据
    # 如果execute()括号内只传一个参数,我们运行 execute(sql)
    # 如果execute()括号内传两个参数,我们运行 execute(sql,params)
    def find_one(self, sql, params=None):
        try:
            if params is None:
                self.count = self.cursor.execute(sql)
            elif params is not None:
                self.count = self.cursor.execute(sql, params)
            return self.cursor.fetchone()  # 返回结果集中的一条数据
        except Exception as e:
            print("查询数据库数据失败!", e)
        # finally:
        #     self.cursor.close()
        #     self.conn.close()

    # 封装查询所有数据: 要求返回具体的数据
    def find_all(self, sql, params=None):
        try:
            if params is None:
                self.count = self.cursor.execute(sql)
            elif params is not None:
                self.count = self.cursor.execute(sql, params)
            return self.cursor.fetchall()  # 返回结果集中的一条数据
        except Exception as e:
            print("查询数据库数据失败!", e)
        # finally:
        #     self.cursor.close()
        #     self.conn.close()


if __name__ == '__main__':
    db = DBUtils()
    a = db.find_all("select * from compute_images;")
    print(a)
    # db.close()
