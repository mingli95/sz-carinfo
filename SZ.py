# -*- coding:utf-8 -*-
#Time:2017-4-27
#
#author:LiMing
import requests
import re,os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator


class Sz_car:
    def __init__(self):
        pass
    # 定义一个标准URL
    def Url(self,args=""):
        url="http://xqctk.sztb.gov.cn/gbl/index%s.html"%(args)
        return url
    # 发起一个标准的http get请求
    def Geturl(self,url):
        r = requests.get(url)
        r.encoding='utf-8'
        html=r.text
        return html
    #获取分页数
    def Page(self):
        url = self.Url()
        html = self.Geturl(url)
        page_re=u'<b>共<span class="f_orange">(.*?)</span>页/共'
        m = re.findall(page_re,html)
        return int(m[0])+1
    #获取每期摇号结果公告url链接
    def Data(self,url):
        html = self.Geturl(url)
        Re=u"""<a class="text" href="(.*?)" target="_blank">深圳市(.*?)普通小汽车增量指标摇号结果公告</a>"""
        m = re.findall(Re,html)
        return m
    # 根据摇号url获取pdf路径
    def Getpdf(self,url):
        html=self.Geturl(url)
        Re=u'href="http://xqctk.sztb.gov.cn/attachment(.*?)pdf"'
        m = re.findall(Re,html)
        m1=[]
        m2=[]
        for i in m:
            url="http://xqctk.sztb.gov.cn/attachment%spdf"%i
            m1.append(url)
        m2=[{u"个人指标":m1[0]},{u"单位指标":m1[1]}]
        return m2

    def Download(self,url):
        r = requests.get(url)
        with open("pdf\\"+url.split('/')[-1],'wb') as code:
            code.write(r.content)
            print u"%s 下载成功!"% url.split('/')[-1]

    def Pdf2txt(self,pdf):
        Dir=ur"D:\django\python2\test08\深圳小汽车摇号结果查询\pdf\\"
        fp = open(Dir+pdf, 'rb')
        #来创建一个pdf文档分析器
        parser = PDFParser(fp)
        #创建一个PDF文档对象存储文档结构
        document = PDFDocument(parser)
        # 检查文件是否允许文本提取
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            # 创建一个PDF资源管理器对象来存储共赏资源
            rsrcmgr=PDFResourceManager()
            # 设定参数进行分析
            laparams=LAParams()
            # 创建一个PDF设备对象
            # device=PDFDevice(rsrcmgr)
            device=PDFPageAggregator(rsrcmgr,laparams=laparams)
            # 创建一个PDF解释器对象
            interpreter=PDFPageInterpreter(rsrcmgr,device)
            # 处理每一页
            for page in PDFPage.create_pages(document):
                interpreter.process_page(page)
                # 接受该页面的LTPage对象
                layout=device.get_result()
                for x in layout:
                    if(isinstance(x,LTTextBoxHorizontal)):
                        with open("txt\\"+pdf.split(".")[0]+".txt",'a') as f:
                            f.write(x.get_text().encode('utf-8')+'\n')
            print u"%s to txt 成功!"%pdf
    def grep_txt(self,txt):
        import sqlite3
        cx = sqlite3.connect(ur"D:\django\python2\test08\深圳小汽车摇号结果查询\car.db")
        cu = cx.cursor()

        Dir=ur"D:\django\python2\test08\深圳小汽车摇号结果查询\txt\\"
        f = open(Dir+txt,'r')
        list=[]
        for i in f.readlines():
            if "本期描述" in i:
                Date=i.split("本期描述：")[-1].split("指标")[0]
            ii = i.split()
            if len(ii) == 3:
                list.append(ii)
            else:
                continue
        # ff = open('sql.txt','a')
        for ii in list:
            if ii[1] != "申请编码":
                sql="INSERT INTO info ( date, name, code) VALUES ('%s','%s','%s');" % (Date,ii[2],ii[1])
                cu.execute(sql)
                # ff.write(sql)
        # ff.close()
        cx.commit()
        f.close()

    def db(self,sql):
        import sqlite3
        import MySQLdb
        cx = sqlite3.connect(ur"D:\django\python2\test08\深圳小汽车摇号结果查询\car.db")
        # cx = MySQLdb.connect("192.168.1.180", "liming", "asdasd123", "db")
        cu = cx.cursor()
        cu.execute(sql)
        cx.commit()


if __name__ == "__main__":
    main=Sz_car()
    # txt="1448532199756.txt"
    # main.grep_txt(txt)
    sql="""
    CREATE TABLE info (
  `date` VARCHAR(45) NULL,
  `name` VARCHAR(45) NULL,
  `code` VARCHAR(45) NULL);"""
    main.db(sql)