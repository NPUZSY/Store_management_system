from tkinter import *
import Client_Buy as Cb
import Client_Login as Cl
import Client_Check_Store as Ccs
import Client_Sell as Cs
from SQL import MyDb


class Windows(object):
    def __init__(self):
        # 初始化界面
        self.is_running = True
        self.is_Log_In = True
        self.root = Tk()
        self.root.title('进销存系统')

        screenwidth = self.root.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.root.winfo_screenheight()  # 屏幕高度
        width = 190
        height = 240
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        self.whichwindows = 0
        # 连接数据库
        lb1 = Label(self.root, text='正在连接数据库……')
        lb1.grid(column=0, row=0)
        self.db = MyDb()
        lb1.configure(text='请选择要使用的功能', font=('Arial', 15),)
        btn_pur = Button(self.root, text="入库登记", command=self.Click_btn_pur)
        btn_sell = Button(self.root, text="出库登记", command=self.Click_btn_sell)
        btn_stock = Button(self.root, text="库存查询", command=self.Click_btn_stock)
        btn_logout = Button(self.root, text="注销", command=self.Click_btn_logout)
        btn_exit = Button(self.root, text="退出", command=self.Click_btn_exit)
        # 这里需要插入一个费用录入按钮 fee 按钮
        btn_pur.place(x=60, y=50)
        btn_sell.place(x=60, y=100)
        btn_stock.place(x=60, y=150)
        btn_logout.place(x=30, y=200)
        btn_exit.place(x=110, y=200)
        self.root.mainloop()

    def upload(self, table, dic):
        # print(dic)
        self.db.upload(table, dic)

    def query(self):
        return self.db.query()

    def Click_btn_pur(self):
        self.whichwindows = 1
        self.root.destroy()

    def Click_btn_sell(self):
        self.whichwindows = 2
        self.root.destroy()

    def Click_btn_stock(self):
        self.whichwindows = 3
        self.root.destroy()

    def Click_btn_logout(self):
        self.is_Log_In = False
        self.root.destroy()

    def Click_btn_exit(self):
        self.is_Log_In = False
        self.is_running = False
        self.root.destroy()


def main():
    is_running = True
    while is_running:
        # 整个程序的循环，方便注销后依然能够进入系统
        is_Log_In, is_running = Cl.Log_In_main()
        while is_Log_In:
            root = Windows()
            is_Log_In = root.is_Log_In
            is_running = root.is_running
            print(is_Log_In, is_running)
            if not is_running and is_Log_In:
                break
            task_Choose = root.whichwindows
            if task_Choose == 1:
                print(task_Choose)
                buy = Cb.Buy()
                form = buy.filling()
                if form:
                    root.upload('tb_buy', form)
                # is_running = False
                # is_Log_In = False
                # break
            elif task_Choose == 2:
                print(task_Choose)
                is_quare = True
                while is_quare:
                    temp = root.query()
                    Sell = Cs.Sell(temp)
                    select = Sell.selected
                    if select:
                        root.db.delete(select)
                    is_quare = Sell.is_quare
                # is_Log_In = False
                # break
            elif task_Choose == 3:
                print(task_Choose)
                is_check = True
                while is_check:
                    temp = root.query()
                    Store = Ccs.Store(temp)
                    is_check = Store.is_check
            else:
                continue


if __name__ == '__main__':
    main()
