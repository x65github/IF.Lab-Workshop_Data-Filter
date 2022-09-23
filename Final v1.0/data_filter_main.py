# -*- coding: utf-8 -*-
from glob import glob
from os import path
import pathlib
from data_filter_pdf import getmaxtxt,dopdf,author_maybe,getkw,getab,iftime,getdoi,writemeta

def ifitem(status,maintxt,metaitems): 
    '''功能Menu'''
    if status == 'abstract': #判斷摘要
        abstract=getab(maintxt)
        print('abstract:',abstract)
        metaitems['Abstract']=abstract
    elif status == 'keywords': #判斷keywords
        maintxt=maintxt.split("[page:")[0]
        keywords=getkw(maintxt) 
        print('keywords:',keywords) 
        metaitems['Keywords']=keywords
    elif 'author' in status : #判斷作者，參數是'author'+maintxt和title_list
        maintxt=maintxt.split("[page:")[0]
        title_list=maintxt
        maintxt=status[6:]
        author=author_maybe(maintxt,title_list)
        print('author:',author)  #保留...以表示並非列出所有作者
        metaitems['Author']=author
    elif status == 'time': #判斷發佈時間
        maintxt=maintxt.split("[page:")[0]
        date=iftime(maintxt)
        print('date：',date)
        metaitems[' Date']=date
    else: #判斷doi
        maintxt=maintxt.split("[page:")[0]
        doi=getdoi(maintxt)
        print('doi：',doi)
        metaitems['DOI']=doi
    return metaitems

def main(pattern_in,pattern_out):
    maintxt=""
    if pattern_in=="here":
        pattern=str(pathlib.Path().absolute())
        pattern_in=pattern+"\\"

    if pattern_out=="here":
        pattern=str(pathlib.Path().absolute())
        pattern_out=pattern+"\\" 

    files = [ path.basename(x) for x in glob(pattern_in+"*.pdf")] #取得所有PDF的檔名
    for i in range(0,len(files)):
        pdf_document = files[i]
        print(pdf_document,"：")
        metaitems={'Producer':'https://github.com/x65github/IF.Lab-Workshop_Data-Filter'}
        try:
            rt=dopdf(pattern_in,pdf_document) #抓特定內容及判斷總頁數
            pages=rt[0]
            lcpage=rt[1]
            maintxt=rt[2]
            metaitems['Pages']=pages
        except Exception as e:
            print('此論文無法開啟，錯誤原因：',e)
            continue
        iftitle(pattern_in,pdf_document,lcpage,maintxt)

def iftitle(pattern_in,pdf_document,lcpage,maintxt):
        try:
            rt=getmaxtxt(pattern_in+pdf_document,lcpage) #判斷標題(回傳list型態的各行標題)
            title_list=rt[0]
            title=rt[1]
            metaitems['Title']=title
        except Exception as e:
            print('此論文無法判斷標題，錯誤原因：',e)
    
        '''判斷剩餘項目'''
        metaitems=ifitem('abstract',maintxt,metaitems)
        metaitems=ifitem('keywords',maintxt,metaitems)
        metaitems=ifitem('author'+maintxt,title_list,metaitems) 
        metaitems=ifitem('time',maintxt,metaitems) 
        metaitems=ifitem('doi',maintxt,metaitems)
        writemeta(pattern_out,pattern_in,pdf_document,metaitems)
    
pattern_in = input("請輸入pdf來源(輸入here為現在所在路徑):")  
pattern_out = input("請輸入pdf目的地(輸入here為現在所在路徑):")
main(pattern_in,pattern_out)
