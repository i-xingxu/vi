# coding=utf-8
import time
import xlrd
import os
import glob
from common import conf
from common import logoutput

class Time():
    '''
    工具模块，时间类
    '''
    def get_now_time(self):
        '''
        获取当前时间，以字符串格式返回
        :return:
        '''
        nowtime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
        return nowtime

class Excel():
    '''
    用来操作Excel
    '''
    def __init__(self):
        self.lg=logoutput.Logger()

    def excelRead(self,path):
        CONF_NAME_EXCELPATH="ExcelPath"
        CONF_NAME_XLSNAME="xlsname"
        CONF_NAME_SHEETNAME="sheetname"

        '''

        :param path: 配置文件所在路径
        :return:返回table
        '''
        try:
            cf=conf.Conf()
            d=cf.get_conf_data(CONF_NAME_EXCELPATH)
            # os.chdir(d["xfpath"])
            data = xlrd.open_workbook(CONF_NAME_XLSNAME)
            table = data.sheet_by_name(CONF_NAME_SHEETNAME)  #通过名称获取
            return table
        except Exception as e:
            self.lg.error(e)

class ResultChinese():

    def get_report_dir(self):
        pyfiles=glob.glob(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\report\\*.xml")
        if not pyfiles:
            return False
        else:
            return pyfiles

    def switch_result(self):
        pathList=self.get_report_dir()
        if pathList:
            p=list(pathList)[0]
            f=open(p,"r",encoding="utf-8")
            r=f.read()
            r=r.encode("unicode_escape")
            r=r.replace(b"\\\\u",b"\\u")
            r=r.decode("unicode_escape","ignore")
            f.close()
            f1=open(p,"w",encoding="utf-8")
            f1.write(str(r))
            f1.close()
        else:
            lg=logoutput.Logger()
            lg.error("未找到测试结果文件！")

if __name__ == '__main__':
    rc=ResultChinese()
    rc.switch_result()
    # print(a)