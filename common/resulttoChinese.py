#coding=utf-8
import glob
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import logoutput

class ResultChinese():

    def __init__(self):
        self.lg=logoutput.Logger()

    def get_report_dir(self):
        pyfiles=glob.glob(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\report\\*.xml")
        if not pyfiles:
            return False
        else:
            return pyfiles

    def switch_result(self):
        pathList=self.get_report_dir()
        if pathList:
            pathList=list(pathList)
            for p in pathList:
                try:
                    f=open(p,"r",encoding="utf-8")
                    r=f.read()
                    r=r.encode("unicode_escape")
                    r=r.replace(b"\\\\u",b"\\u")
                    r=r.decode("unicode_escape","ignore")
                    f.close()
                    f1=open(p,"w",encoding="utf-8")
                    f1.write(str(r))
                    f1.close()
                    self.lg.info("转换测试结果中的unicode")
                except:
                    continue
        else:
            self.lg.error("未找到测试结果文件！")

if __name__ == '__main__':
    rc=ResultChinese()
    rc.switch_result()
    # print(a)