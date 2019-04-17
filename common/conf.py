#coding=utf-8
import configparser,os,sys


class NewConfigParser(configparser.ConfigParser):
    '''
    继承配置文件类，重写optionform方法，使返回值区分大小写。
    '''
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        '''
        重写方法，返回值区分大小写
        :param optionstr:
        :return:
        '''
        return optionstr


class Conf():
    '''
    使用继承后的配置文件类
    '''

    def __init__(self,path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\conf"):
        CONF_FILE_NAME="test.conf"
        self.path=path+"\\"+CONF_FILE_NAME


    def get_conf_data(self,name):
        '''
        获取配置文件内容
        :param path: 配置文件路径
        :return:
        '''
        try:
            cf=NewConfigParser()
            cf.read(self.path,"utf-8")
            cf.sections()
            confData=cf.options(name)
            cfData={}
            for i in range(0,len(confData)):
                cfData[confData[i]]=cf.get(name,confData[i])
            return cfData
        except Exception as e:
            print(e)
            print("读取配置文件出错！")





# c=Conf()
# d=c.get_conf_data(r"xfXmlPath")
# print(d)