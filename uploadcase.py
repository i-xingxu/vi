# ucoding=utf-8
import xlrd
import os

os.chdir(os.path.split(os.path.realpath(__file__))[0])
from common import mysql
from common import logoutput


class Upload():
    def __init__(self):
        self.lg = logoutput.Logger()
        # 打开excel表格
        try:
            # data = xlrd.open_workbook(path)
            self.open_excel()
            self.table = self.data.sheet_by_index(0)
            self.ROW_COUNT = self.table.nrows
        except Exception as e:
            self.lg.error(e)
            self.lg.error("打开Excel表格失败！")
        # 数据库连接
        try:
            self.db = mysql.Mysql()
            self.db.connect_mysql()
        except Exception as e:
            self.lg.error(e)
            self.lg.error("连接数据库失败！")

    # 插入数据
    def insert_case(self):
        datas = self.get_excel_data()
        # res=self.casename_is_repetition(data)
        try:
            # cols=self.get_casename()
            for data in datas:
                # 查询用例名称是否存在，返回结果为空则插入用例名称，再插入测试数据，若结果不为空，则提示已存在，向对应名称中继续添加数据
                self.db.cur.execute(
                    "select * from case_name where case_name=\"{}\" and pid=\"{}\"".format(data[1], data[0]))
                res = self.db.cur.fetchall()
                # id=self.db.cur.execute("select id from case_name where case_name=\"{}\"".format(data[1]))
                try:
                    # for i in range(0,len(data)):
                    #     if type(data[i])==float:
                    #         data[i]=int(data[i])
                    if res:
                        self.lg.info("用例名称已存在：{}，将继续向对应名称添加测试数据".format(data[1]))
                        self.insert_case_data(data)
                    else:
                        # self.lg.error(e)
                        sql = "insert into case_name(case_name,pid) values (\"{}\",\"{}\")".format(data[1], data[0])
                        self.db.cur.execute(sql)
                        self.lg.info("插入一条用例名称：{}".format(data[1]))
                        self.insert_case_data(data)
                        # self.update_case(id,data)
                except Exception as e:
                    self.lg.error(e)
        except Exception as e:
            self.lg.error(e)

    def get_excel_data(self):
        # 获取每一行数据
        for i in range(1, self.ROW_COUNT):
            data = self.table.row_values(i)
            for j in range(0, len(data)):
                # for j in range(0,len(d)):
                if type(data[j]) == float:
                    data[j] = int(data[j])
            # 判断每个单元格长度
            if len(str(data[0])) < 11 and len(str(data[1])) < 20 and len(str(data[2])) < 100 and len(
                    str(data[3])) < 100:
                # 生成器
                yield data
            else:
                self.lg.error("数据长度过长，跳过导入！\"{}\"".format(data))
                continue

    def update_case(self):
        # 这是用update语句更新
        # datas=self.get_excel_data()
        # for data in datas:
        #     for i in range(0,len(data)):
        #          if type(data[i])==float:
        #              data[i]=int(data[i])
        #     self.db.cur.execute("select id from case_name where case_name=\"{}\"".format(data[1]))
        #     id=self.db.cur.fetchall()
        #     if res==1:
        #         sql="update test_data set imput_data=\"{}\",except_data=\"{}\" where cid=\"{}\"".format(data[2],data[3],id[0][0])
        #         self.db.cur.execute(sql)
        #         self.lg.info("更新用例名称：\"{}\"的数据：\"{}\"".format(data[1],data[2]))
        #     elif res==0:
        #         pass
        # 更新用例采用的是先删除后插入的方法，删除对应用例名称的用例名称和数据，再重新导入
        datas = self.get_excel_data()
        for data in datas:
            res = [data[1], data[0]]
            self.delete_case(res)
        self.insert_case()

    def delete_case(self, res):
        # 先查询用例名称是否存在，若存在，删除，不存在给出提示重新输入
        ui = UI()
        sqlSelect = "select id from case_name where case_name=\"{}\" and pid=\"{}\"".format(res[0], res[1])
        self.db.cur.execute(sqlSelect)
        id = self.db.cur.fetchall()
        if len(id) == 0:
            print("输入的用例名称不存在，请重新输入！")
            # res = ui.delete_ui()
            # self.delete_case(res)
        else:
            sql = "delete from case_name where case_name=\"{}\"".format(res[0])
            self.db.cur.execute(sql)
            self.db.cur.execute("delete from test_data where cid=\"{}\"".format(id[0][0]))
            self.lg.info("删除用例：{}".format(res))
            # ui.delete_ui()

    def insert_case_data(self, data):
        try:
            self.db.cur.execute("select id from case_name where case_name=\"{}\"".format(data[1]))
            id = self.db.cur.fetchall()
            sqlData = "insert into test_data(cid,imput_data,except_data) values (\"{}\",\"{}\",\"{}\")".format(id[0][0],
                                                                                                               data[2],
                                                                                                               data[3])
            self.db.cur.execute(sqlData)
            self.lg.info("插入一条用例数据，数据：{}，预期结果：{}".format(data[2], data[3]))
        except Exception as e:
            self.lg.error(e)

    def open_excel(self):
        ui = UI()
        path = ui.open_ui()
        try:
            self.data = xlrd.open_workbook(path)
            # return data
        except:
            print("请输入正确的地址！")
            self.open_excel()

    def main(self):
        ui = UI()
        # up=Upload()
        while (1):
            n = ui.start()
            if n == "1":
                self.insert_case()
            if n == "2":
                res = ui.update_ui()
                self.update_case()
            if n == "3":
                res = ui.delete_ui()
                # self.delete_case()
            if n == "4":
                up.db.close_connect()
                os._exit(0)

    def close_connect(self):
        self.db.close_connect()


class UI():
    # 在二级菜单，输入0返回到一级
    def __init__(self):
        self.lg = logoutput.Logger()
        # self.up=Upload()

    def start(self):
        while (1):
            print("请输入对应操作的数字：")
            print("1.导入用例")
            print("2.更新用例")
            print("3.删除用例")
            print("4.退出")
            number = input("请输入1~4：")
            if number == str(1):
                return number
            elif number == str(2):
                return number
            elif number == str(3):
                return number
            elif number == str(4):
                return number
            else:
                print("输入错误，请重新输入！")

    def update_ui(self):
        while (1):
            print("是否更新用例？y/n\n输入0返回上一级")
            res = input("请输入y或n：")
            if res == "y" or res == "Y":
                return 1
            elif res == "n" or res == "N":
                return 0
            elif res == "0":
                up.main()
            else:
                print("请输入y或n")
                self.update_ui()

    def delete_ui(self):
        # 输入用例名称和平台编码，删除对应用例，输入0返回上一级
        # print("将要删除用例！")
        # up=Upload()
        res = input("请输入要删除的用例名称和平台对应编码，以空格分隔\n1--学法平台\n2--电商\n3--云平台:\n输入0返回上一级\n")
        try:
            if res == "0":
                up.main()
            else:
                res = res.split(" ")
                try:
                    if res[0] != "" and len(res[0]) < 20 and res[1] != "":
                        up.delete_case(res)
                        self.delete_ui()
                    # elif res[0]=="0":
                    #     up.main()
                    else:
                        self.delete_ui()
                except:
                    self.lg.error("请按格式输入！！")
                    self.delete_ui()
        except:
            self.lg.error("请按格式输入！")
            self.delete_ui()

    def open_ui(self):
        # print()
        path = input("请输入excel地址，例：D:\excel.xls\n")
        return path


if __name__ == "__main__":

    ui = UI()
    # path=input("请输入excel文件地址：\n")
    up = Upload()
    print("!!!!!!!!!!!!!!注意事项！!!!!!!!!!!!!!!!!")
    print(
        "1）用例数据中\";\"符号为分隔符，用来分隔用例输入数据，如：用户名1;密码1;\n2）本工具依赖于common包，需与common包在同一级目录下\n3）上传文件格式为.xls或.xlsx文件\n4）插入数据，指的是将excel表中数据插入到数据库中，每一个平台的用例名称唯一，一个用例名称可以对应多组数据\n5）更新用例，指的是将excel表中的用例名称所对应的用例数据删除，并重新导入新的数据\n6）删除数据,输入用例名称和平台对应编码，即可正常删除")
    try:
        up.main()
        # ui.start()
    finally:
        up.db.close_connect()
