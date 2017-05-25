# -*- coding:utf-8 -*-
#Time:2017-4-27
#
#author:LiMing
"""
1.获取所有通知公告url。
2.根据公告信息获取所有摇号结果指标url。
3.获取每期摇号结果的个人和单位结果pdf url。
4.下载个人和单位pdf 文件。
"""
import SZ,os
# 1.获取所有url。
def all_url():
    urllist=[]
    for i in range(1,main.Page()):
        if i==1:
            urllist.append(main.Url())
        else:
            urllist.append(main.Url(args="_%s"%i))
    return urllist
# 2.根据公告信息获取所有摇号结果指标url。
def zhibiao_url(urllist):
    dic = {}
    for i in urllist:
        for ii in main.Data(i):
            dic[ii[1]]=ii[0]
    return dic
# 3.获取每期摇号结果的个人和单位结果pdf url。
def pdf_url():
    All_url=all_url()
    urllist=zhibiao_url(All_url)
    dic={}
    for k,v in urllist.items():
        info = main.Getpdf(v)
        dic[k]={"url":v,u"个人指标":info[0][u"个人指标"],u"单位指标":info[1][u"单位指标"]}
    return dic
# 4.下载个人和单位pdf 文件。
def download_pdf():
    info = pdf_url()
    for k,v in info.items():
        main.Download(v[u'个人指标'])
        main.Download(v[u'单位指标'])

def pdf2txt():
    Dir=ur"D:\django\python2\test08\深圳小汽车摇号结果查询\pdf"
    listfile=os.listdir(Dir)
    for i in listfile:
        main.Pdf2txt(i)
def save_data():
    Dir=ur"D:\django\python2\test08\深圳小汽车摇号结果查询\txt"
    listfile=os.listdir(Dir)
    for i in listfile:
        main.grep_txt(i)

if __name__ == "__main__":
    main = SZ.Sz_car()
    # download_pdf()
    # pdf2txt()
    save_data()