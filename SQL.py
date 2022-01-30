import pymysql
from datetime import datetime


class MyDb(object):
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(host='39.99.159.98',
                                  user='finance',
                                  password='finance',
                                  database='Finance_DB')
        self.cursor = self.db.cursor()
        self.dic = {}
        self.delete_id = ''
        # print('连接数据库成功')

    def execute(self, task):
        # 执行SQL语句 以字符串形式传入
        # self.cursor.execute("use Finance_DB;")
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(task)
            self.cursor.connection.commit()
        except:
            self.db.rollback()
        self.cursor.close()

    def upload(self, table, dic):
        print('开始上载数据')
        default = 0
        if not dic['规格型号']:
            dic['规格型号'] = '个'
        if not dic['含税进价']:
            dic['含税进价'] = default
        if not dic['未税进价']:
            dic['未税进价'] = default
        # keys = 'id，kind，name，source，model，unit，quantity，cost_withtax，cost_withouttax'
        tt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        task = 'insert into {} ' \
               'values({},"{}","{}","{}","{}","{}","{}",' \
               '"{}",{},{},{},{},"{}");'.format(table,
                                                dic['商品编号'],
                                                dic['日期'],
                                                dic['往来单位'],
                                                dic['一级分类'],
                                                dic['二级分类'],
                                                dic['商品名称'],
                                                dic['规格型号'],
                                                dic['单位'],
                                                dic['数量'],
                                                dic['含税进价'],
                                                dic['未税进价'],
                                                dic['实际进价'],
                                                dic['备注/序列号'])
        # print(task)
        self.execute(task)

        # print('上载数据成功')
        self.dic = dic
        self.refresh_store('add')

    def query(self):
        self.execute("select * from tb_buy;")
        temp = self.cursor.fetchall()
        # print(temp)
        return temp

    def delete(self, datas):
        task = 'delete from tb_buy where id in ({});'.format(datas)
        self.execute(task)
        # print(task)
        # print('出库成功')
        self.delete_id = datas
        self.refresh_store('delete')

    def refresh_store(self, method):
        """根据入库信息和出库信息刷新库存单"""
        print('刷新库存', method)
        if method == 'add':
            print(self.dic)


def main():
    MDB = MyDb()
    # MDB.execute('CREATE TABLE EMPLOYEE (FIRST_NAME  CHAR(20) NOT NULL,'
    #             'LAST_NAME  CHAR(20),AGE INT,SEX CHAR(1),INCOME FLOAT )')


if __name__ == '__main__':
    main()
